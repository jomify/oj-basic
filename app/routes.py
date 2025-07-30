from datetime import datetime
from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from .models import User, Problem, TestCase, Submission, Exam, ExamProblem
from .utils import compile_and_run


def register_routes(app):
    @app.route('/')
    def index():
        problems = Problem.query.all()
        exams = Exam.query.order_by(Exam.start_time.desc()).all()
        return render_template('index.html', problems=problems, exams=exams, user=session.get('user'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = generate_password_hash(request.form['password'])
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return redirect(url_for('register'))
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user'] = {'id': user.id, 'username': user.username, 'is_admin': user.is_admin}
                return redirect(url_for('index'))
            flash('Invalid credentials')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('user', None)
        return redirect(url_for('index'))

    @app.route('/problems/<int:pid>')
    def problem(pid):
        prob = Problem.query.get_or_404(pid)
        exam_id = request.args.get('exam')
        return render_template('problem.html', problem=prob, exam_id=exam_id, user=session.get('user'))

    @app.route('/submit/<int:pid>', methods=['GET', 'POST'])
    def submit(pid):
        prob = Problem.query.get_or_404(pid)
        exam_id = request.args.get('exam') or request.form.get('exam_id')
        if request.method == 'POST':
            code = request.form['code']
            user_id = session.get('user', {}).get('id')
            if not user_id:
                flash('Please login to submit')
                return redirect(url_for('login'))
            for case in TestCase.query.filter_by(problem_id=pid).all():
                ok, output = compile_and_run(code, case.input_data)
                if not ok:
                    result = f'Error: {output.strip()}'
                    break
                if output.strip() != case.expected_output.strip():
                    result = 'Wrong Answer'
                    break
            else:
                result = 'Accepted'
            submission = Submission(user_id=user_id, problem_id=pid, code=code,
                                   result=result, exam_id=exam_id)
            db.session.add(submission)
            db.session.commit()
            flash(f'Result: {result}')
            if exam_id:
                return redirect(url_for('exam', eid=exam_id))
            return redirect(url_for('problem', pid=pid))
        return render_template('submit.html', problem=prob, exam_id=exam_id, user=session.get('user'))

    @app.route('/submissions')
    def submissions():
        user_id = session.get('user', {}).get('id')
        if not user_id:
            flash('Please login to view submissions')
            return redirect(url_for('login'))
        subs = Submission.query.filter_by(user_id=user_id).all()
        return render_template('submissions.html', submissions=subs, user=session.get('user'))

    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        user = session.get('user')
        if not user or not user.get('is_admin'):
            flash('Admin only')
            return redirect(url_for('index'))
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            input_desc = request.form['input_desc']
            output_desc = request.form['output_desc']
            sample_input = request.form['sample_input']
            sample_output = request.form['sample_output']
            prob = Problem(title=title, description=description, input_desc=input_desc,
                           output_desc=output_desc, sample_input=sample_input, sample_output=sample_output)
            db.session.add(prob)
            db.session.commit()
            flash('Problem added')
        problems = Problem.query.all()
        return render_template('admin.html', problems=problems, user=user)

    @app.route('/admin/problem/<int:pid>/testcases', methods=['GET', 'POST'])
    def manage_testcases(pid):
        user = session.get('user')
        if not user or not user.get('is_admin'):
            flash('Admin only')
            return redirect(url_for('index'))
        prob = Problem.query.get_or_404(pid)
        if request.method == 'POST':
            input_data = request.form['input_data']
            expected_output = request.form['expected_output']
            tc = TestCase(problem_id=pid, input_data=input_data, expected_output=expected_output)
            db.session.add(tc)
            db.session.commit()
            flash('Test case added')
        testcases = TestCase.query.filter_by(problem_id=pid).all()
        return render_template('admin_testcase.html', problem=prob, testcases=testcases, user=user)

    @app.route('/admin/exam', methods=['GET', 'POST'])
    def admin_exam():
        user = session.get('user')
        if not user or not user.get('is_admin'):
            flash('Admin only')
            return redirect(url_for('index'))
        if request.method == 'POST':
            title = request.form['title']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            exam = Exam(title=title, start_time=start_time, end_time=end_time)
            db.session.add(exam)
            db.session.commit()
            flash('Exam created')
        exams = Exam.query.all()
        return render_template('admin_exam.html', exams=exams, user=user)

    @app.route('/exam/<int:eid>')
    def exam(eid):
        exam = Exam.query.get_or_404(eid)
        now = datetime.utcnow()
        started = now >= exam.start_time
        ended = now >= exam.end_time
        problems = [ep.problem for ep in ExamProblem.query.filter_by(exam_id=eid).all()]
        return render_template('exam.html', exam=exam, problems=problems, started=started, ended=ended, user=session.get('user'))

    @app.route('/exam/<int:eid>/scoreboard')
    def exam_scoreboard(eid):
        exam = Exam.query.get_or_404(eid)
        scores = {}
        submissions = Submission.query.filter_by(exam_id=eid).all()
        for sub in submissions:
            user = User.query.get(sub.user_id)
            if user.username not in scores:
                scores[user.username] = 0
            if sub.result == 'Accepted':
                scores[user.username] += 1
        return render_template('scoreboard.html', exam=exam, scores=scores, user=session.get('user'))
