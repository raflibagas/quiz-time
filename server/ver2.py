from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sablihganteng'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sablih890-@127.0.0.1/mydatabase3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

logging.basicConfig(level=logging.DEBUG)

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    logging.debug(f"Received data: {data}")
    username = data['username']
    password = data['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    if User.query.filter_by(username=username).first():
        logging.debug("User already exists")
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    logging.debug("Registration successful")
    return jsonify({"message": "Registration successful"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid username or password"}), 400

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})

@app.route('/add_question', methods=['POST'])
@login_required
def add_question():
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    subject = data['subject']
    question_text = data['question_text']
    choices = json.dumps(data['choices'])  # Encode choices as JSON
    correct_answer = data['correct_answer']

    new_question = Question(subject=subject, question_text=question_text, choices=choices, correct_answer=correct_answer)
    db.session.add(new_question)
    db.session.commit()

    return jsonify({"message": "Question added successfully"})

@app.route('/get_questions', methods=['GET'])
@login_required
def get_questions():
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized access"}), 403

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

    return jsonify(question_list)

@app.route('/submit_answers', methods=['POST'])
@login_required
def submit_answers():
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    correct_count = 0

    for answer in data['answers']:
        question_id = answer['question_id']
        selected_answer = answer['selected_answer']
        question = Question.query.get(question_id)

        is_correct = selected_answer == question.correct_answer
        if is_correct:
            correct_count += 1

        new_answer = Answer(user_id=current_user.id, question_id=question_id, selected_answer=selected_answer, is_correct=is_correct)
        db.session.add(new_answer)

    db.session.commit()

    return jsonify({"message": "Quiz submitted successfully", "correct_count": correct_count})

@socketio.on('register')
def handle_register(data):
    logging.debug(f"Received data: {data}")
    username = data['username']
    password = data['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    if User.query.filter_by(username=username).first():
        logging.debug("User already exists")
        emit('register_response', {'error': 'User already exists'})
    else:
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        logging.debug("Registration successful")
        emit('register_response', {'message': 'Registration successful'})

@socketio.on('login')
def handle_login(data):
    logging.debug(f"Received data: {data}")
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        emit('login_response', {'message': 'Login successful'})
    else:
        emit('login_response', {'error': 'Invalid username or password'})

@socketio.on('logout')
@login_required
def handle_logout(data):
    logging.debug("Logout event received", data)
    logout_user()
    emit('logout_response', {"message": "Logout successful"})

@socketio.on('add_question')
@login_required
def handle_add_question(data):
    if not current_user.is_authenticated:
        emit('add_question_response', {"error": "Unauthorized access"})
        return

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
    if not current_user.is_authenticated:
        emit('get_questions_response', {"error": "Unauthorized access"})
        return

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
    if not current_user.is_authenticated:
        emit('submit_answers_response', {"error": "Unauthorized access"})
        return

    correct_count = 0

    for answer in data['answers']:
        question_id = answer['question_id']
        selected_answer = answer['selected_answer']
        question = Question.query.get(question_id)

        is_correct = selected_answer == question.correct_answer
        if is_correct:
            correct_count += 1

        new_answer = Answer(user_id=current_user.id, question_id=question_id, selected_answer=selected_answer, is_correct=is_correct)
        db.session.add(new_answer)

    db.session.commit()

    emit('submit_answers_response', {"message": "Quiz submitted successfully", "correct_count": correct_count})

@socketio.on('message')
def handle_message(msg):
    print(f'Message: {msg}')
    emit('response', {'data': msg}, broadcast=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
