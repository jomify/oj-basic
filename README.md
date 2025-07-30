# Simple Java Online Judge

This project provides a minimal Online Judge (OJ) website for evaluating Java code. It supports user registration, problem management, code submission with automatic judging, and simple exam management. The UI uses Bootstrap for a cleaner look.

## Features
- User registration and login
- Submit Java solutions and receive verdicts
- Admin interface to add problems, exams and test cases
- Basic exam mode with start and end times plus a scoreboard
- SQLite database for persistence

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server for development:
   ```bash
   python server.py
   ```
   Or run with Gunicorn for production:
   ```bash
   gunicorn -w 4 server:app
   ```
3. Open `http://localhost:5000` in your browser.

Use the Admin page to create problems, exams and test cases. Sample problems can be inserted by writing scripts using the models in `app/models.py`.
