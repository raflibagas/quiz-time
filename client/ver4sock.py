import tkinter as tk
from tkinter import messagebox, ttk
import socketio

SERVER_URL = "http://192.168.1.101:5000"
sio = socketio.Client()

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("400x300")
        
        # Initialize frames
        self.init_login_frame()

    def init_login_frame(self):
        self.clear_frame()
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        tk.Label(self.login_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.login_frame, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.login_frame, text="Register", command=self.register).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        sio.emit('login', {'username': username, 'password': password})

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        sio.emit('register', {'username': username, 'password': password})

    def init_role_selection_frame(self):
        self.clear_frame()
        self.role_frame = tk.Frame(self.root)
        self.role_frame.pack(pady=20)

        tk.Label(self.role_frame, text="Select Role").pack()
        self.role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(self.role_frame, textvariable=self.role_var, values=["Teacher", "Student"])
        role_dropdown.pack(pady=10)

        tk.Button(self.role_frame, text="Confirm", command=self.confirm_role).pack(pady=10)
        tk.Button(self.role_frame, text="View History", command=self.view_history).pack(pady=10)
        tk.Button(self.role_frame, text="View Logs", command=self.view_logs).pack(pady=10)
        tk.Button(self.role_frame, text="Logout", command=self.logout).pack(pady=10)

    def view_logs(self):
        sio.emit('get_logs', {'dummy': 'data'})

    def init_logs_frame(self, logs):
        self.clear_frame()
        self.logs_frame = tk.Frame(self.root)
        self.logs_frame.pack(pady=20)

        tk.Label(self.logs_frame, text="Server Logs").pack()

        logs_text = tk.Text(self.logs_frame)
        logs_text.pack()
        logs_text.insert(tk.END, "\n".join(logs))

        tk.Button(self.logs_frame, text="Back", command=self.init_role_selection_frame).pack(pady=10)

    def confirm_role(self):
        role = self.role_var.get()
        if role == "Teacher":
            self.init_add_question_frame()
        elif role == "Student":
            self.init_take_quiz_frame()
        else:
            messagebox.showerror("Error", "Please select a valid role.")

    def logout(self):
        print("Logout button pressed")
        sio.emit('logout', {'dummy': 'data'})  # Sending dummy data to satisfy the server's requirement

    def view_history(self):
        sio.emit('get_quiz_history', {'dummy': 'data'})

    def init_history_frame(self, history):
        self.clear_frame()
        self.history_frame = tk.Frame(self.root)
        self.history_frame.pack(pady=20)

        tk.Label(self.history_frame, text="Quiz History").pack()

        for item in history:
            tk.Label(self.history_frame, text=f"Subject: {item['subject']}, Score: {item['score']}, Date: {item['timestamp']}").pack()

        tk.Button(self.history_frame, text="Back", command=self.init_role_selection_frame).pack(pady=10)

    def init_add_question_frame(self):
        self.clear_frame()
        self.add_question_frame = tk.Frame(self.root)
        self.add_question_frame.pack(pady=20)

        tk.Label(self.add_question_frame, text="Select Subject").pack()
        self.subject_var = tk.StringVar()
        subject_dropdown = ttk.Combobox(self.add_question_frame, textvariable=self.subject_var, values=["Math", "Biology"])
        subject_dropdown.pack(pady=10)

        tk.Label(self.add_question_frame, text="Question Text").pack()
        self.question_entry = tk.Entry(self.add_question_frame)
        self.question_entry.pack()

        tk.Label(self.add_question_frame, text="Choices (comma separated)").pack()
        self.choices_entry = tk.Entry(self.add_question_frame)
        self.choices_entry.pack()

        tk.Label(self.add_question_frame, text="Correct Answer").pack()
        self.correct_answer_entry = tk.Entry(self.add_question_frame)
        self.correct_answer_entry.pack()

        tk.Button(self.add_question_frame, text="Add Question", command=self.add_question).pack(pady=10)
        tk.Button(self.add_question_frame, text="Back", command=self.init_role_selection_frame).pack(pady=10)

    def add_question(self):
        subject = self.subject_entry.get()
        question_text = self.question_entry.get()
        choices = self.choices_entry.get().split(',')
        correct_answer = self.correct_answer_entry.get()

        sio.emit('add_question', {
            'subject': subject,
            'question_text': question_text,
            'choices': choices,
            'correct_answer': correct_answer
        })

    def init_take_quiz_frame(self):
        self.clear_frame()
        self.take_quiz_frame = tk.Frame(self.root)
        self.take_quiz_frame.pack(pady=20)

        tk.Label(self.take_quiz_frame, text="Select Subject").pack()
        self.subject_take_var = tk.StringVar()
        subject_take_dropdown = ttk.Combobox(self.take_quiz_frame, textvariable=self.subject_take_var, values=["Math", "Biology"])
        subject_take_dropdown.pack(pady=10)

        tk.Button(self.take_quiz_frame, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.take_quiz_frame, text="Back", command=self.init_role_selection_frame).pack(pady=10)

    def start_quiz(self):
        subject = self.subject_take_var.get()
        sio.emit('get_questions', {'subject': subject})
        self.submitted_answers = []  # Initialize submitted answers list

    def init_quiz_question_frame(self):
        self.clear_frame()
        self.quiz_question_frame = tk.Frame(self.root)
        self.quiz_question_frame.pack(pady=20)

        question_data = self.questions[self.current_question]
        self.current_question_id = question_data['id']

        tk.Label(self.quiz_question_frame, text=f"Question {self.current_question + 1}").pack()
        tk.Label(self.quiz_question_frame, text=question_data['question_text']).pack()

        self.answer_var = tk.StringVar()
        for choice in question_data['choices']:
            tk.Radiobutton(self.quiz_question_frame, text=choice, variable=self.answer_var, value=choice).pack(anchor="w")

        if self.current_question < 9:
            tk.Button(self.quiz_question_frame, text="Next", command=self.next_question).pack(pady=10)
        else:
            tk.Button(self.quiz_question_frame, text="Submit", command=self.submit_quiz).pack(pady=10)

    def next_question(self):
        selected_answer = self.answer_var.get()
        self.submitted_answers.append({
            'question_id': self.current_question_id,
            'selected_answer': selected_answer
        })
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.init_quiz_question_frame()
        else:
            self.submit_quiz()

    def submit_quiz(self):
        selected_answer = self.answer_var.get()
        self.submitted_answers.append({
            'question_id': self.current_question_id,
            'selected_answer': selected_answer
        })
        sio.emit('submit_answers', {'answers': self.submitted_answers})

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Socket.IO event handlers
@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('login_response')
def on_login_response(data):
    if 'message' in data:
        messagebox.showinfo("Login Successful", data["message"])
        app.init_role_selection_frame()
    else:
        messagebox.showerror("Login Failed", data["error"])

@sio.on('register_response')
def on_register_response(data):
    if 'message' in data:
        messagebox.showinfo("Registration Successful", data["message"])
    else:
        messagebox.showerror("Registration Failed", data["error"])

@sio.on('logout_response')
def on_logout_response(data):
    print("Logout response received:", data)
    if 'message' in data:
        messagebox.showinfo("Logout Successful", data["message"])
        app.init_login_frame()
    else:
        messagebox.showerror("Logout Failed", data["error"])

@sio.on('add_question_response')
def on_add_question_response(data):
    if 'message' in data:
        messagebox.showinfo("Success", data["message"])
    else:
        messagebox.showerror("Error", data["error"])

@sio.on('get_questions_response')
def on_get_questions_response(data):
    app.questions = data
    app.current_question = 0
    app.correct_count = 0
    app.init_quiz_question_frame()

@sio.on('submit_answers_response')
def on_submit_answers_response(data):
    if 'message' in data:
        if data.get('correct_count') is not None:
            app.correct_count = data['correct_count']
        messagebox.showinfo("Quiz Completed", f"You answered {app.correct_count} questions correctly!")
        app.init_role_selection_frame()
    else:
        messagebox.showerror("Error", data["error"])

@sio.on('quiz_history_response')
def on_quiz_history_response(data):
    app.init_history_frame(data)

@sio.on('logs_response')
def on_logs_response(data):
    app.init_logs_frame(data)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    sio.connect(SERVER_URL)
    root.mainloop()
    sio.disconnect()
