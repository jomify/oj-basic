import os
import subprocess
import tempfile
import shutil


def compile_and_run(code, input_data, timeout=5):
    temp_dir = tempfile.mkdtemp()
    try:
        source_path = os.path.join(temp_dir, 'Main.java')
        with open(source_path, 'w') as f:
            f.write(code)
        compile_proc = subprocess.run(['javac', source_path], capture_output=True, text=True, timeout=timeout)
        if compile_proc.returncode != 0:
            return False, compile_proc.stderr
        run_proc = subprocess.run(['java', '-cp', temp_dir, 'Main'], input=input_data, capture_output=True, text=True, timeout=timeout)
        if run_proc.returncode != 0:
            return False, run_proc.stderr
        return True, run_proc.stdout
    except subprocess.TimeoutExpired:
        return False, 'Time Limit Exceeded'
    finally:
        shutil.rmtree(temp_dir)
