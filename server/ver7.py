from flask import Flask, request, jsonify, g
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from logging.handlers import RotatingFileHandler
import json
import datetime
import pytz
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sablihganteng'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sablih890-@127.0.0.1/mydatabase3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Ensure the user_logs directory exists
if not os.path.exists('user_logs'):
    os.makedirs('user_logs')

# Function to get user-specific logger
def get_user_logger(user_id):
    user_logger = logging.getLogger(f"user_{user_id}")
    if not user_logger.hasHandlers():
        handler = RotatingFileHandler(f'user_logs/user_{user_id}.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        handler.setFormatter(formatter)
        user_logger.addHandler(handler)
        user_logger.setLevel(logging.DEBUG)
    return user_logger

# Add a stream handler to the app logger for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
console_handler.setFormatter(formatter)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.DEBUG)

@app.before_request
def log_request_info():
    g.start = datetime.datetime.now()
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Request Headers: {request.headers}")
        g.user_logger.debug(f"Request Body: {request.get_data()}")
    app.logger.debug(f"Request Headers: {request.headers}")
    app.logger.debug(f"Request Body: {request.get_data()}")

@app.after_request
def log_response_info(response):
    duration = datetime.datetime.now() - g.start
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Response Status: {response.status}")
        g.user_logger.debug(f"Response Body: {response.get_data()}")
        g.user_logger.debug(f"Duration: {duration}")
    app.logger.debug(f"Response Status: {response.status}")
    app.logger.debug(f"Response Body: {response.get_data()}")
    app.logger.debug(f"Duration: {duration}")
    return response

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(150), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    choices = db.Column(db.Text, nullable=False)  # JSON encoded choices
    correct_answer = db.Column(db.String(150), nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_answer = db.Column(db.String(150), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

class QuizHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    app.logger.debug(f"Received data: {data}")
    username = data['username']
    password = data['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    if User.query.filter_by(username=username).first():
        app.logger.debug("User already exists")
        response = jsonify({"error": "User already exists"}), 400
        app.logger.debug(f"Response: {response}")
        return response

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    response = jsonify({"message": "Registration successful"})
    app.logger.debug(f"Response: {response}")
    return response

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    app.logger.debug(f"Received data: {data}")
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        g.user_logger = get_user_logger(user.id)
        g.user_logger.debug("Login successful")
        response = jsonify({"message": "Login successful"})
    else:
        response = jsonify({"error": "Invalid username or password"}), 400

    app.logger.debug(f"Response: {response}")
    return response

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug("Logout successful")
    logout_user()
    response = jsonify({"message": "Logout successful"})
    app.logger.debug(f"Response: {response}")
    return response

@app.route('/add_question', methods=['POST'])
@login_required
def add_question():
    data = request.get_json()
    app.logger.debug(f"Received data: {data}")
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Received data: {data}")

    subject = data['subject']
    question_text = data['question_text']
    choices = json.dumps(data['choices'])  # Encode choices as JSON
    correct_answer = data['correct_answer']

    new_question = Question(subject=subject, question_text=question_text, choices=choices, correct_answer=correct_answer)
    db.session.add(new_question)
    db.session.commit()

    response = jsonify({"message": "Question added successfully"})
    app.logger.debug(f"Response: {response}")
    if current_user.is_authenticated:
        g.user_logger.debug(f"Response: {response}")
    return response

@app.route('/get_questions', methods=['GET'])
@login_required
def get_questions():
    app.logger.debug(f"Received data: {request.args}")
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Received data: {request.args}")

    subject = request.args.get('subject')
    questions = Question.query.filter_by(subject=subject).order_by(db.func.random()).limit(10).all()

    question_list = []
    for question in questions:
        question_data = {
            'id': question.id,
            'question_text': question.question_text,
            'choices': json.loads(question.choices)  # Decode choices from JSON
        }
        question_list.append(question_data)

    response = jsonify(question_list)
    app.logger.debug(f"Response: {response}")
    if current_user.is_authenticated:
        g.user_logger.debug(f"Response: {response}")
    return response

@app.route('/submit_answers', methods=['POST'])
@login_required
def submit_answers():
    data = request.get_json()
    app.logger.debug(f"Received data: {data}")
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Received data: {data}")

    correct_count = 0
    subject = None

    for answer in data['answers']:
        question_id = answer['question_id']
        selected_answer = answer['selected_answer']
        question = db.session.get(Question, question_id)

        if not subject:
            subject = question.subject

        is_correct = selected_answer == question.correct_answer
        if is_correct:
            correct_count += 1

        new_answer = Answer(user_id=current_user.id, question_id=question_id, selected_answer=selected_answer, is_correct=is_correct)
        db.session.add(new_answer)

    db.session.commit()

    # Save quiz history with UTC+7 timezone
    utc_now = datetime.datetime.utcnow()
    utc_plus_7 = utc_now + datetime.timedelta(hours=7)
    quiz_history = QuizHistory(user_id=current_user.id, subject=subject, score=correct_count, timestamp=utc_plus_7)
    db.session.add(quiz_history)
    db.session.commit()

    response = jsonify({"message": "Quiz submitted successfully", "correct_count": correct_count})
    app.logger.debug(f"Response: {response}")
    if current_user.is_authenticated:
        g.user_logger.debug(f"Response: {response}")
    return response

@app.route('/quiz_history', methods=['GET'])
@login_required
def get_quiz_history():
    app.logger.debug(f"Received data: {request.args}")
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Received data: {request.args}")

    user_id = current_user.id
    history = QuizHistory.query.filter_by(user_id=user_id).all()
    history_list = [
        {
            'id': h.id,
            'subject': h.subject,
            'score': h.score,
            'timestamp': h.timestamp.astimezone(pytz.timezone('Asia/Jakarta')).strftime('%Y-%m-%d %H:%M:%S')
        } for h in history
    ]

    response = jsonify(history_list)
    app.logger.debug(f"Response: {response}")
    if current_user.is_authenticated:
        g.user_logger.debug(f"Response: {response}")
    return response

@app.route('/logs', methods=['GET'])
@login_required
def get_logs():
    user_id = current_user.id
    try:
        with open(f'user_logs/user_{user_id}.log', 'r') as f:
            log_data = f.read()
        response = jsonify(log_data.split('\n'))
    except FileNotFoundError:
        response = jsonify({"error": "No logs available for this user"}), 404

    app.logger.debug(f"Response: {response}")
    return response

@socketio.on('register')
def handle_register(data):
    app.logger.debug(f"Received data: {data}")
    username = data['username']
    password = data['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    if User.query.filter_by(username=username).first():
        app.logger.debug("User already exists")
        emit('register_response', {'error': 'User already exists'})
    else:
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        app.logger.debug("Registration successful")
        emit('register_response', {'message': 'Registration successful'})

@socketio.on('login')
def handle_login(data):
    app.logger.debug(f"Received data: {data}")
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        g.user_logger = get_user_logger(user.id)
        g.user_logger.debug("Login successful")
        emit('login_response', {'message': 'Login successful'})
    else:
        emit('login_response', {'error': 'Invalid username or password'})

@socketio.on('logout')
@login_required
def handle_logout(data):
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug("Logout event received")
    logout_user()
    emit('logout_response', {"message": "Logout successful"})

@socketio.on('add_question')
@login_required
def handle_add_question(data):
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Received data: {data}")

    subject = data['subject']
    question_text = data['question_text']
    choices = json.dumps(data['choices'])
    correct_answer = data['correct_answer']

    new_question = Question(subject=subject, question_text=question_text, choices=choices, correct_answer=correct_answer)
    db.session.add(new_question)
    db.session.commit()

    emit('add_question_response', {"message": "Question added successfully"})

@socketio.on('get_questions')
@login_required
def handle_get_questions(data):
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Received data: {data}")

    subject = data['subject']
    questions = Question.query.filter_by(subject=subject).order_by(db.func.random()).limit(10).all()

    question_list = []
    for question in questions:
        question_data = {
            'id': question.id,
            'question_text': question.question_text,
            'choices': json.loads(question.choices)
        }
        question_list.append(question_data)

    emit('get_questions_response', question_list)

@socketio.on('submit_answers')
@login_required
def handle_submit_answers(data):
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Received data: {data}")

    correct_count = 0
    subject = None

    for answer in data['answers']:
        question_id = answer['question_id']
        selected_answer = answer['selected_answer']
        question = db.session.get(Question, question_id)

        if not subject:
            subject = question.subject

        is_correct = selected_answer == question.correct_answer
        if is_correct:
            correct_count += 1

        new_answer = Answer(user_id=current_user.id, question_id=question_id, selected_answer=selected_answer, is_correct=is_correct)
        db.session.add(new_answer)

    db.session.commit()

    # Save quiz history with UTC+7 timezone
    utc_now = datetime.datetime.utcnow()
    utc_plus_7 = utc_now + datetime.timedelta(hours=7)
    quiz_history = QuizHistory(user_id=current_user.id, subject=subject, score=correct_count, timestamp=utc_plus_7)
    db.session.add(quiz_history)
    db.session.commit()

    emit('submit_answers_response', {"message": "Quiz submitted successfully", "correct_count": correct_count})

@socketio.on('get_quiz_history')
@login_required
def handle_get_quiz_history(data):
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Received data: {data}")

    user_id = current_user.id
    history = QuizHistory.query.filter_by(user_id=user_id).all()
    history_list = [
        {
            'id': h.id,
            'subject': h.subject,
            'score': h.score,
            'timestamp': h.timestamp.astimezone(pytz.timezone('Asia/Jakarta')).strftime('%Y-%m-%d %H:%M:%S')
        } for h in history
    ]
    emit('quiz_history_response', history_list)

@socketio.on('get_logs')
@login_required
def handle_get_logs(data):
    user_id = current_user.id
    try:
        with open(f'user_logs/user_{user_id}.log', 'r') as f:
            log_data = f.read()
        emit('logs_response', log_data.split('\n'))
    except FileNotFoundError:
        emit('logs_response', {"error": "No logs available for this user"})

@socketio.on('message')
def handle_message(msg):
    if current_user.is_authenticated:
        g.user_logger = get_user_logger(current_user.id)
        g.user_logger.debug(f"Received message: {msg}")
    emit('response', {'data': msg}, broadcast=True)

@socketio.on_error_default
def default_error_handler(e):
    app.logger.error(f'SocketIO error: {e}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
