import tkinter as tk
from tkinter import messagebox, ttk, Canvas, PhotoImage
import socketio
import threading
import logging
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\data dari laptop sewa\client-quiz\assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

SERVER_URL = "http://10.8.107.202:5000"
sio = socketio.Client()

class Main_window:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("512x384")
        self.window.configure(bg="#FFFFFF")

        # Variabel untuk menampung isi textbox pada halaman login
        self.login_username = tk.StringVar()
        self.login_password = tk.StringVar()

        # Variabel untuk menampung isi textbox pada halaman register
        self.register_username = tk.StringVar()
        self.register_password = tk.StringVar()

        # Variabel untuk enampung username untuk halaman setelah sign in
        self.logged_in_username = ""

        # Variabel untuk menampung hasil pemilihan role
        self.role_chosen = tk.StringVar()

        # Variabel untuk menampung hasil pemilihan subject
        self.subject_chosen = tk.StringVar()

        self.timer_running = False
        self.quiz_submitted = False

        # Page awal
        self.show_sign_in_page()

        self.window.resizable(True, True)
        # self.window.mainloop()

    def delete_frame(self):
        for frame in self.window.winfo_children():
            frame.destroy()

    def show_sign_up_page(self):
        self.window.title("Sign Up Page")
        self.sign_up_frame = tk.Frame(self.window, width=512, height=384)

        self.canvas = Canvas(self.sign_up_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.sign_up_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        self.sign_up_title_text = ttk.Label(self.sign_up_frame, text="Sign Up", background="#D9D9D9", foreground="#000000",
                                            font=("Inter", 32 * -1))
        self.sign_up_title_text.place(x=194.0, y=102.0)

        self.new_account_text = ttk.Label(self.sign_up_frame, text="Have an account?", background="#D9D9D9", foreground="#000000",
                                          font=("Inter", 12 * -1))
        self.new_account_text.place(x=168.0, y=260.0)

        self.sign_in_text = ttk.Label(self.sign_up_frame, text="Sign in here", background="#D9D9D9", foreground="#0084FF",
                                      font=("Inter", 12 * -1), cursor="hand2")
        self.sign_in_text.place(x=270.0, y=260.0)

        def to_sign_in_page(event):
            self.password_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.delete_frame()
            self.show_sign_in_page()

        def bold_sign_in_text(event):
            self.sign_in_text.configure(font=("Inter", 12 * -1, 'bold'))

        def normalize_sign_in_text(event):
            self.sign_in_text.configure(font=("Inter", 12 * -1))

        self.sign_in_text.bind("<Button-1>", to_sign_in_page)
        self.sign_in_text.bind("<Enter>", bold_sign_in_text)
        self.sign_in_text.bind("<Leave>", normalize_sign_in_text)

        self.username_entry = ttk.Entry(self.sign_up_frame, textvariable=self.register_username, foreground="gray")
        self.username_entry.place(x=156.0, y=152.0, width=200.0, height=40.0)
        self.username_entry.insert(0, "Username")

        def username_in_focus(event):
            if self.register_username.get() == "Username":
                self.username_entry.delete(0, tk.END)
                self.username_entry.configure(foreground="black")

        def username_out_focus(event):
            if self.register_username.get() == "":
                self.username_entry.insert(0, "Username")
                self.username_entry.configure(foreground="gray")

        self.username_entry.bind("<FocusIn>", username_in_focus)
        self.username_entry.bind("<FocusOut>", username_out_focus)

        self.password_entry = ttk.Entry(self.sign_up_frame, textvariable=self.register_password, foreground="gray")
        self.password_entry.place(x=156.0, y=208.0, width=200.0, height=40.0)
        self.password_entry.insert(0, "Password")

        def password_in_focus(event):
            if self.register_password.get() == "Password":
                self.password_entry.delete(0, tk.END)
                self.password_entry.configure(foreground="black", show='*')

        def password_out_focus(event):
            if self.register_password.get() == "":
                self.password_entry.insert(0, "Password")
                self.password_entry.configure(foreground="gray", show='')

        self.password_entry.bind("<FocusIn>", password_in_focus)
        self.password_entry.bind("<FocusOut>", password_out_focus)

        self.register_button_image = PhotoImage(file=relative_to_assets("register_button.png"))
        self.register_button = tk.Button(self.sign_up_frame, image=self.register_button_image, borderwidth=0, highlightthickness=0,
                                         command=self.register, relief="flat", cursor="hand2")
        self.register_button.image = self.register_button_image
        self.register_button.place(x=156.0, y=285.0, width=200.0, height=40.0)

        self.sign_up_frame.place(x=0, y=0)

    def show_sign_in_page(self):
        self.window.title("Sign In Page")
        self.sign_in_frame = tk.Frame(self.window, width=512, height=384)

        self.canvas = Canvas(self.sign_in_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.sign_in_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        self.sign_in_title_text = ttk.Label(self.sign_in_frame, text="Sign In", background="#D9D9D9", foreground="#000000",
                                            font=("Inter", 32 * -1))
        self.sign_in_title_text.place(x=204.0, y=102.0)

        self.new_account_text = ttk.Label(self.sign_in_frame, text="New account?", background="#D9D9D9", foreground="#000000",
                                          font=("Inter", 12 * -1))
        self.new_account_text.place(x=180.0, y=260.0)

        self.sign_up_text = ttk.Label(self.sign_in_frame, text="Sign up here", background="#D9D9D9", foreground="#0084FF",
                                      font=("Inter", 12 * -1), cursor="hand2")
        self.sign_up_text.place(x=260.0, y=260.0)

        def to_sign_up_page(event):
            self.password_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.delete_frame()
            self.show_sign_up_page()

        def bold_sign_up_text(event):
            self.sign_up_text.configure(font=("Inter", 12 * -1, 'bold'))

        def normalize_sign_up_text(event):
            self.sign_up_text.configure(font=("Inter", 12 * -1))

        self.sign_up_text.bind("<Button-1>", to_sign_up_page)
        self.sign_up_text.bind("<Enter>", bold_sign_up_text)
        self.sign_up_text.bind("<Leave>", normalize_sign_up_text)

        self.username_entry = ttk.Entry(self.sign_in_frame, textvariable=self.login_username, foreground="gray")
        self.username_entry.place(x=156.0, y=152.0, width=200.0, height=40.0)
        self.username_entry.insert(0, "Username")

        def username_in_focus(event):
            if self.login_username.get() == "Username":
                self.username_entry.delete(0, tk.END)
                self.username_entry.configure(foreground="black")

        def username_out_focus(event):
            if self.login_username.get() == "":
                self.username_entry.insert(0, "Username")
                self.username_entry.configure(foreground="gray")

        self.username_entry.bind("<FocusIn>", username_in_focus)
        self.username_entry.bind("<FocusOut>", username_out_focus)

        self.password_entry = ttk.Entry(self.sign_in_frame, textvariable=self.login_password, foreground="gray")
        self.password_entry.place(x=156.0, y=208.0, width=200.0, height=40.0)
        self.password_entry.insert(0, "Password")

        def password_in_focus(event):
            if self.login_password.get() == "Password":
                self.password_entry.delete(0, tk.END)
                self.password_entry.configure(foreground="black", show='*')

        def password_out_focus(event):
            if self.login_password.get() == "":
                self.password_entry.insert(0, "Password")
                self.password_entry.configure(foreground="gray", show='')

        self.password_entry.bind("<FocusIn>", password_in_focus)
        self.password_entry.bind("<FocusOut>", password_out_focus)

        self.sign_in_button_image = PhotoImage(file=relative_to_assets("sign_in_button.png"))
        self.sign_in_button = tk.Button(self.sign_in_frame, image=self.sign_in_button_image, borderwidth=0, highlightthickness=0,
                                        command=self.login, relief="flat", cursor="hand2")
        self.sign_in_button.image = self.sign_in_button_image
        self.sign_in_button.place(x=156.0, y=285.0, width=200.0, height=40.0)

        self.sign_in_frame.place(x=0, y=0)

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        sio.emit('login', {'username': username, 'password': password})

    def register(self):
        username = self.register_username.get()
        password = self.register_password.get()
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        sio.emit('register', {'username': username, 'password': password})

    def role_choosing_page(self):
        self.clear_frame()
        self.window.title("Choose Role")
        self.role_choosing_frame = tk.Frame(self.window, width=512, height=384)

        self.canvas = Canvas(self.role_choosing_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.role_choosing_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        self.username_text = ttk.Label(self.role_choosing_frame, text=f"Hi, {self.logged_in_username}",
                                       background="#28003A", foreground="#FFFFFF", font=("Inter", 12 * -1), anchor=tk.E)
        self.username_text.place(x=150.0, y=10.0, width=350.0, height=16.0)

        self.choose_role_title_text = ttk.Label(self.role_choosing_frame, text="Choose Role", background="#D9D9D9", foreground="#000000",
                                                font=("Inter", 20 * -1))
        self.choose_role_title_text.place(x=195.0, y=104.0)

        role_options = ["Student", "Teacher"]
        self.role_dropdown = ttk.OptionMenu(self.role_choosing_frame, self.role_chosen, role_options[0], *role_options)
        self.role_dropdown.place(x=156.0, y=152.0, width=200.0, height=40.0)

        self.view_log = tk.Button(self.role_choosing_frame, text="View Logs", command=self.view_logs, cursor="hand2")

        self.view_log.place(x=220.0, y=300.0, width=66.0, height=22.0)

        self.role_confirm_button_image = PhotoImage(file=relative_to_assets("role_confirm_button.png"))
        self.role_confirm_button = tk.Button(self.role_choosing_frame, image=self.role_confirm_button_image, borderwidth=0,
                                             highlightthickness=0, command=self.role_confirm_callback, relief="flat", cursor="hand2")
        self.role_confirm_button.image = self.role_confirm_button_image
        self.role_confirm_button.place(x=188.0, y=260.0, width=135.0, height=21.0)

        self.sign_out_button_image = PhotoImage(file=relative_to_assets("sign_out_button.png"))
        self.sign_out_button = tk.Button(self.role_choosing_frame, image=self.sign_out_button_image, borderwidth=0, highlightthickness=0,
                                         command=self.logout, relief="flat", cursor="hand2")
        self.sign_out_button.place(x=433.0, y=35.0, width=66.0, height=22.0)

        self.role_choosing_frame.place(x=0.0, y=0.0)

    def role_confirm_callback(self):
        if self.role_chosen.get() == "Student":
            self.init_student_role_frame()
        else:
            self.delete_frame()
            self.add_question_page()

    def logout(self):
        sio.emit('logout', {})

    def view_history(self):
        sio.emit('get_quiz_history', {})
    
    def view_logs(self):
        sio.emit('get_logs', {'dummy': 'data'})

    def init_logs_frame(self, logs):
        self.clear_frame()
        self.logs_frame = tk.Frame(self.window)
        self.logs_frame.pack(pady=20)

        tk.Label(self.logs_frame, text="Server Logs").pack()

        logs_text = tk.Text(self.logs_frame)
        logs_text.pack()
        logs_text.insert(tk.END, "\n".join(logs))

        tk.Button(self.logs_frame, text="Back", command=self.role_choosing_page).pack(pady=10)

    def init_student_role_frame(self):
        self.clear_frame()
        self.student_role_frame = tk.Frame(self.window, width=512, height=384)
        self.student_role_frame.pack(pady=20)

        tk.Button(self.student_role_frame, text="Take Quiz", command=self.init_take_quiz_frame).pack(pady=10)
        tk.Button(self.student_role_frame, text="View History", command=self.view_history).pack(pady=10)
        tk.Button(self.student_role_frame, text="Back", command=self.role_choosing_page).pack(pady=10)

    def init_history_frame(self, history):
        self.clear_frame()
        self.history_frame = tk.Frame(self.window, width=512, height=384)
        self.history_frame.pack(pady=20)

        tk.Label(self.history_frame, text="Quiz History").pack()

        for item in history:
            tk.Label(self.history_frame, text=f"Subject: {item['subject']}, Score: {item['score']}, Date: {item['timestamp']}").pack()

        tk.Button(self.history_frame, text="Back", command=self.init_student_role_frame).pack(pady=10)

    def add_question_page(self):
        self.window.title("Add Question")
        self.add_question_frame = tk.Frame(self.window, width=512, height=384)

        self.canvas = Canvas(self.add_question_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.add_question_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        self.username_text = ttk.Label(self.add_question_frame, text=f"Hi, {self.logged_in_username}",
                                       background="#28003A", foreground="#FFFFFF", font=("Inter", 12 * -1), anchor=tk.E)
        self.username_text.place(x=150.0, y=10.0, width=350.0, height=16.0)

        self.select_subject_text = ttk.Label(self.add_question_frame, text="Select Subject", background="#D9D9D9", foreground="#000000",
                                             font=("Inter", 12 * -1))
        self.select_subject_text.place(x=214.0, y=100.0)

        subject_options = ["Mathematics", "Biology"]
        self.subject_dropdown = ttk.OptionMenu(self.add_question_frame, self.subject_chosen, subject_options[0], *subject_options)
        self.subject_dropdown.place(x=196.0, y=118.0, width=120.0, height=20.0)

        self.question_text = ttk.Label(self.add_question_frame, text="Question", background="#D9D9D9", foreground="#000000",
                                       font=("Inter", 12 * -1))
        self.question_text.place(x=230.0, y=139.0)

        self.question_entry = tk.Text(self.add_question_frame, foreground="gray", font=("Segoe UI", 10))
        self.question_entry.place(x=149.0, y=156.0, width=214.0, height=80.0)
        self.question_entry.insert(0.0, "E.g. What is the value of sine of 90 degrees?")

        def question_in_focus(event):
            if self.question_entry.get("1.0", "end-1c") == "E.g. What is the value of sine of 90 degrees?":
                self.question_entry.delete(0.0, tk.END)
                self.question_entry.configure(foreground="black")

        def question_out_focus(event):
            if self.question_entry.get("1.0", "end-1c") == "":
                self.question_entry.insert(0.0, "E.g. What is the value of sine of 90 degrees?")
                self.question_entry.configure(foreground="gray")

        self.question_entry.bind("<FocusIn>", question_in_focus)
        self.question_entry.bind("<FocusOut>", question_out_focus)

        self.choices_text = ttk.Label(self.add_question_frame, text="Choices (Comma-separated)", background="#D9D9D9", foreground="#000000",
                                      font=("Inter", 12 * -1))
        self.choices_text.place(x=78.0, y=243.0)

        self.choice_entry = tk.Text(self.add_question_frame, foreground="gray", font=("Segoe UI", 10))
        self.choice_entry.place(x=91.0, y=261.0, width=140.0, height=40.0)
        self.choice_entry.insert(0.0, "E.g. 0,1,-1,2")

        def choice_in_focus(event):
            if self.choice_entry.get("1.0", "end-1c") == "E.g. 0,1,-1,2":
                self.choice_entry.delete(0.0, tk.END)
                self.choice_entry.configure(foreground="black")

        def choice_out_focus(event):
            if self.choice_entry.get("1.0", "end-1c") == "":
                self.choice_entry.insert(0.0, "E.g. 0,1,-1,2")
                self.choice_entry.configure(foreground="gray")

        self.choice_entry.bind("<FocusIn>", choice_in_focus)
        self.choice_entry.bind("<FocusOut>", choice_out_focus)

        self.correct_answer_text = ttk.Label(self.add_question_frame, text="Correct Answer", background="#D9D9D9", foreground="#000000",
                                             font=("Inter", 12 * -1))
        self.correct_answer_text.place(x=307.0, y=243.0)

        self.correct_answer_entry = tk.Text(self.add_question_frame, foreground="gray", font=("Segoe UI", 10))
        self.correct_answer_entry.place(x=282.0, y=261.0, width=140.0, height=40.0)
        self.correct_answer_entry.insert(0.0, "E.g. 1")

        def correct_answer_in_focus(event):
            if self.correct_answer_entry.get("1.0", "end-1c") == "E.g. 1":
                self.correct_answer_entry.delete(0.0, tk.END)
                self.correct_answer_entry.configure(foreground="black")

        def correct_answer_out_focus(event):
            if self.correct_answer_entry.get("1.0", "end-1c") == "":
                self.correct_answer_entry.insert(0.0, "E.g. 1")
                self.correct_answer_entry.configure(foreground="gray")

        self.correct_answer_entry.bind("<FocusIn>", correct_answer_in_focus)
        self.correct_answer_entry.bind("<FocusOut>", correct_answer_out_focus)

        self.add_question_button_image = PhotoImage(file=relative_to_assets("add_question_button.png"))
        self.add_question_button = tk.Button(self.add_question_frame, image=self.add_question_button_image, borderwidth=0, highlightthickness=0,
                                             command=self.add_question, relief="flat")
        self.add_question_button.image = self.add_question_button_image
        self.add_question_button.place(x=188.0, y=316.0, width=135.0, height=22.0)

        self.sign_out_button_image = PhotoImage(file=relative_to_assets("sign_out_button.png"))
        self.sign_out_button = tk.Button(self.add_question_frame, image=self.sign_out_button_image, borderwidth=0, highlightthickness=0,
                                         command=self.logout, relief="flat", cursor="hand2")
        self.sign_out_button.place(x=433.0, y=35.0, width=66.0, height=22.0)

        self.back_add_question_button_image = PhotoImage(file=relative_to_assets("back_add_question_button.png"))
        self.back_add_question_button = tk.Button(self.add_question_frame, image=self.back_add_question_button_image, borderwidth=0, highlightthickness=0,
                                                  command=self.role_choosing_page, relief="flat")
        self.back_add_question_button.image = self.back_add_question_button_image
        self.back_add_question_button.place(x=83.0, y=103.0, width=66.0, height=22.0)

        self.add_question_frame.place(x=0.0, y=0.0)

    def add_question(self):
        subject = self.subject_chosen.get()
        question_text = self.question_entry.get("1.0", "end-1c")
        choices = self.choice_entry.get("1.0", "end-1c").split(',')
        correct_answer = self.correct_answer_entry.get("1.0", "end-1c")

        if not subject or not question_text or not choices or not correct_answer:
            messagebox.showerror("Error", "Fields cannot be empty.")
            return

        sio.emit('add_question', {
            'subject': subject,
            'question_text': question_text,
            'choices': choices,
            'correct_answer': correct_answer
        })

    def init_take_quiz_frame(self):
        self.clear_frame()
        self.take_quiz_frame = tk.Frame(self.window, width=512, height=384)
        self.take_quiz_frame.pack(pady=20)

        tk.Label(self.take_quiz_frame, text="Select Subject").pack()
        self.subject_take_var = tk.StringVar()
        subject_take_dropdown = ttk.Combobox(self.take_quiz_frame, textvariable=self.subject_take_var, values=["Math", "Biology"])
        subject_take_dropdown.pack(pady=10)

        tk.Button(self.take_quiz_frame, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(self.take_quiz_frame, text="Back", command=self.init_student_role_frame).pack(pady=10)

    def start_quiz(self):
        subject = self.subject_take_var.get()
        if not subject:
            messagebox.showerror("Error", "Subject cannot be empty.")
            return
        sio.emit('get_questions', {'subject': subject})

    def start_timer(self):
        self.timer_seconds = 300  # 5 minutes
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running and not self.quiz_submitted:
            minutes, seconds = divmod(self.timer_seconds, 60)
            time_format = '{:02d}:{:02d}'.format(minutes, seconds)
            self.timer_label.config(text=time_format)
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.window.after(1000, self.update_timer)
            else:
                self.submit_quiz()

    def init_quiz_question_frame(self):
        self.clear_frame()
        self.quiz_question_frame = tk.Frame(self.window, width=512, height=384)
        self.quiz_question_frame.pack(pady=20)

        self.timer_label = tk.Label(self.quiz_question_frame, text="", font=("Helvetica", 16))
        self.timer_label.pack(pady=10, anchor="e", padx=10)

        if not self.timer_running:
            self.start_timer()

        question_data = self.questions[self.current_question]
        self.current_question_id = question_data['id']

        tk.Label(self.quiz_question_frame, text=f"Question {self.current_question + 1}").pack()
        tk.Label(self.quiz_question_frame, text=question_data['question_text']).pack()

        self.answer_var = tk.StringVar()
        for choice in question_data['choices']:
            tk.Radiobutton(self.quiz_question_frame, text=choice, variable=self.answer_var, value=choice).pack(anchor="w")

        if self.current_question < len(self.questions) - 1:
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
        if not self.timer_running or self.quiz_submitted:
            return
        self.timer_running = False
        self.quiz_submitted = True

        selected_answer = self.answer_var.get()
        self.submitted_answers.append({
            'question_id': self.current_question_id,
            'selected_answer': selected_answer
        })
        sio.emit('submit_answers', {'answers': self.submitted_answers})

    def clear_frame(self):
        for widget in self.window.winfo_children():
            widget.destroy()


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
        app.logged_in_username = app.login_username.get()
        app.username_entry.delete(0, tk.END)
        app.password_entry.delete(0, tk.END)
        app.delete_frame()
        app.role_choosing_page()
    else:
        messagebox.showerror("Login Failed", data["error"])


@sio.on('register_response')
def on_register_response(data):
    if 'message' in data:
        messagebox.showinfo("Registration Successful", data["message"])
        app.username_entry.delete(0, tk.END)
        app.password_entry.delete(0, tk.END)
        app.delete_frame()
        app.show_sign_in_page()
    else:
        messagebox.showerror("Registration Failed", data["error"])


@sio.on('logout_response')
def on_logout_response(data):
    if 'message' in data:
        messagebox.showinfo("Logout Successful", data["message"])
        app.delete_frame()
        app.show_sign_in_page()
    else:
        messagebox.showerror("Logout Failed", data["error"])


@sio.on('add_question_response')
def on_add_question_response(data):
    if 'message' in data:
        messagebox.showinfo("Success", data["message"])
        app.question_entry.delete("1.0", tk.END)
        app.question_entry.insert("1.0", "E.g. What is the value of sine of 90 degrees?")
        app.question_entry.configure(foreground="gray")
        app.choice_entry.delete("1.0", tk.END)
        app.choice_entry.insert("1.0", "E.g. 0,1,-1,2")
        app.choice_entry.configure(foreground="gray")
        app.correct_answer_entry.delete("1.0", tk.END)
        app.correct_answer_entry.insert("1.0", "E.g. 1")
        app.correct_answer_entry.configure(foreground="gray")
    else:
        messagebox.showerror("Error", data["error"])


@sio.on('get_questions_response')
def on_get_questions_response(data):
    app.questions = data
    app.current_question = 0
    app.correct_count = 0
    app.submitted_answers = []
    app.timer_running = False
    app.quiz_submitted = False
    app.init_quiz_question_frame()


@sio.on('submit_answers_response')
def on_submit_answers_response(data):
    if 'message' in data:
        if data.get('correct_count') is not None:
            app.correct_count = data['correct_count']
        messagebox.showinfo("Quiz Completed", f"You answered {app.correct_count} questions correctly!")
        app.init_student_role_frame()
    else:
        messagebox.showerror("Error", data["error"])


@sio.on('quiz_history_response')
def on_quiz_history_response(data):
    app.init_history_frame(data)

@sio.on('logs_response')
def on_logs_response(data):
    app.init_logs_frame(data)


if __name__ == "__main__":
    # threading.Thread(target=lambda: sio.connect(SERVER_URL), daemon=True).start()
    app = Main_window()

    sio.connect(SERVER_URL)
    
    app.window.mainloop()
    sio.disconnect()
