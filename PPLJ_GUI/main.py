from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import Tk, Canvas, Text, Button, PhotoImage, ttk, messagebox


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Python\PPLJ_GUI\assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Main_window:
    # Constructor
    def __init__(self):
        # Inisialisasi window
        self.window = Tk()
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

        # Variabel untuk menampung hasil pemilihan subject (teacher)
        self.subject_chosen = tk.StringVar()

        # Variabel untuk menampung hasil pemilihan subject (student)
        self.subject_quiz = tk.StringVar()

        # Page awal
        self.show_sign_in_page()
        # self.role_choosing_page()

        self.window.resizable(False, False)
        self.window.mainloop()
    # Fungsi-fungsi
    # Fungsi untuk destroy semua frame
    def delete_frame(self):
        for frame in self.window.winfo_children():
            frame.destroy()

    # Fungsi untuk halaman sign up
    def show_sign_up_page(self):
        # Judul window
        self.window.title("Sign Up Page")

        # Membuat Frame
        self.sign_up_frame = tk.Frame(self.window, width=512, height=384)

        # Membuat canvas
        self.canvas = Canvas(self.sign_up_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # Membuat kotak background krem
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")

        # Insert logo di kiri atas
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.sign_up_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        # Insert teks judul sign up
        self.sign_up_title_text = ttk.Label(self.sign_up_frame, text="Sign Up", background="#D9D9D9", foreground="#000000",
                                       font=("Inter", 32 * -1))
        self.sign_up_title_text.place(x=194.0, y=102.0)

        # Insert teks have an account?
        self.new_account_text = ttk.Label(self.sign_up_frame, text="Have an account?", background="#D9D9D9", foreground="#000000",
                                     font=("Inter", 12 * -1))
        self.new_account_text.place(x=168.0, y=260.0)

        # Insert teks sign in now, mengarah ke page sign in
        self.sign_in_text = ttk.Label(self.sign_up_frame, text="Sign in here", background="#D9D9D9", foreground="#0084FF",
                                 font=("Inter", 12 * -1), cursor="hand2")
        self.sign_in_text.place(x=270.0, y=260.0)

        def to_sign_in_page(event):
            # Ke halaman sign in
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

        # ==================================Bagian Entry Username=================================
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
        # ========================================================================================

        # ==================================Bagian Entry Password================================
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
        # ========================================================================================

        # ==================================Bagian Sign In========================================
        self.register_button_image = PhotoImage(file=relative_to_assets("register_button.png"))
        self.register_button = Button(self.sign_up_frame, image=self.register_button_image, borderwidth=0, highlightthickness=0,
                                 command=lambda: sign_in_callback(), relief="flat", cursor="hand2")
        self.register_button.image = self.register_button_image
        self.register_button.place(x=156.0, y=285.0, width=200.0, height=40.0)

        def sign_in_callback():
            if self.register_username.get() == "Username" or self.register_password.get() == "Password":
                msg = messagebox.showerror("Notice", "Username or Password empty or invalid!")
            else:
                msg = messagebox.showinfo("Notice", "Registered!\nPress OK to continue")
                if msg == "ok":
                    # Masuk ke halaman sign in
                    self.password_entry.delete(0, tk.END)
                    self.username_entry.delete(0, tk.END)
                    self.delete_frame()
                    self.show_sign_in_page()

        # ========================================================================================
        self.sign_up_frame.place(x=0, y=0)

    # Fungsi untuk halaman sign in
    def show_sign_in_page(self):
        # Judul window
        self.window.title("Sign In Page")

        # Membuat Frame
        self.sign_in_frame = tk.Frame(self.window, width=512, height=384)

        # Membuat canvas
        self.canvas = Canvas(self.sign_in_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)

        # Membuat kotak background krem
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")

        # Insert logo di kiri atas
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.sign_in_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        # Insert teks judul sign in
        self.sign_in_title_text = ttk.Label(self.sign_in_frame, text="Sign In", background="#D9D9D9",foreground="#000000",font=("Inter", 32 * -1))
        self.sign_in_title_text.place(x=204.0, y=102.0)

        # Insert teks New account?
        self.new_account_text = ttk.Label(self.sign_in_frame, text="New account?", background="#D9D9D9",foreground="#000000",font=("Inter", 12 * -1))
        self.new_account_text.place(x=180.0, y=260.0)

        # Insert teks sign up now, mengarah ke page sign up
        self.sign_up_text = ttk.Label(self.sign_in_frame, text="Sign up here", background="#D9D9D9",foreground="#0084FF",font=("Inter", 12 * -1), cursor="hand2")
        self.sign_up_text.place(x=260.0, y=260.0)

        def to_sign_up_page(event):
            # Ke halaman sign up
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

        # ==================================Bagian Entry Username=================================
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
        # ========================================================================================

        # ==================================Bagian Entry Password================================
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
        # ========================================================================================

        # ==================================Bagian Sign In========================================
        self.sign_in_button_image = PhotoImage(file=relative_to_assets("sign_in_button.png"))
        self.sign_in_button = Button(self.sign_in_frame, image=self.sign_in_button_image, borderwidth=0,highlightthickness=0,command=lambda: sign_in_callback(), relief="flat", cursor="hand2")
        self.sign_in_button.image = self.sign_in_button_image
        self.sign_in_button.place(x=156.0, y=285.0, width=200.0, height=40.0)

        def sign_in_callback():
            if self.login_username.get() == "Username" or self.login_password.get() == "Password":
                msg = messagebox.showerror("Notice", "Username or Password empty or invalid!")
            else:
                msg = messagebox.showinfo("Notice", "Signed in!\nPress OK to continue")
                if msg == "ok":
                    # masuk ke halaman pilih role (client)
                    self.logged_in_username = self.login_username.get()
                    self.password_entry.delete(0, tk.END)
                    self.username_entry.delete(0, tk.END)
                    self.delete_frame()
                    self.role_choosing_page()

        # ========================================================================================
        self.sign_in_frame.place(x=0, y=0)

    # Fungsi untuk halaman pemilihan role
    def role_choosing_page(self):
        # Judul window
        self.window.title("Choose Role")

        # Membuat Frame
        self.role_choosing_frame = tk.Frame(self.window, width=512, height=384)

        # Membuat canvas
        self.canvas = Canvas(self.role_choosing_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)

        # Membuat kotak background krem
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")

        # Insert logo di kiri atas
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.role_choosing_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        # Insert username di kanan atas
        self.username_text = ttk.Label(self.role_choosing_frame, text=f"Hi, {self.logged_in_username}",
                                       background="#28003A", foreground="#FFFFFF", font=("Inter", 12 * -1), anchor=tk.E)
        self.username_text.place(x=150.0, y=10.0, width=350.0, height=16.0)

        # Insert teks Choose Role
        self.choose_role_title_text = ttk.Label(self.role_choosing_frame, text="Choose Role", background="#D9D9D9", foreground="#000000",font=("Inter", 20 * -1))
        self.choose_role_title_text.place(x=195.0, y=104.0)

        # Insert dropdown role dengan ttk.OptionMenu
        role_options = ["Student", "Teacher"]
        self.role_dropdown = ttk.OptionMenu(self.role_choosing_frame, self.role_chosen, role_options[0], *role_options)
        self.role_dropdown.place(x=156.0, y=152.0, width=200.0, height=40.0)

        # ======================================Bagian Confirm Role================================================
        self.role_confirm_button_image = PhotoImage(file=relative_to_assets("role_confirm_button.png"))
        self.role_confirm_button = Button(image=self.role_confirm_button_image, borderwidth=0, highlightthickness=0,command=lambda: role_confirm_callback(), relief="flat", cursor="hand2")
        self.role_confirm_button.image = self.role_confirm_button_image
        self.role_confirm_button.place(x=188.0, y=260.0, width=135.0, height=21.0)

        def role_confirm_callback():
            if self.role_chosen.get() == "Student":
                # Ke page memilih soal
                self.delete_frame()
                self.student_home_page()
            else:
                # Ke page upload soal
                self.delete_frame()
                self.add_question_page()
        # =========================================================================================================

        # ======================================Bagian Sign Out================================================
        self.sign_out_button_image = PhotoImage(file=relative_to_assets("sign_out_button.png"))
        self.sign_out_button = Button(image=self.sign_out_button_image, borderwidth=0, highlightthickness=0,command=lambda: sign_out_callback(), relief="flat", cursor="hand2")
        self.sign_out_button.place(x=433.0, y=35.0, width=66.0, height=22.0)
        # =====================================================================================================

        def sign_out_callback():
            # Ke page sign in
            self.delete_frame()
            self.show_sign_in_page()
        # =====================================================================================================
        self.role_choosing_frame.place(x=0.0, y=0.0)

    # Fungsi untuk halaman penambahan soal (teacher)
    def add_question_page(self):
        # Judul window
        self.window.title("Add Question")

        # Membuat Frame
        self.add_question_frame = tk.Frame(self.window, width=512, height=384)

        # Membuat canvas
        self.canvas = Canvas(self.add_question_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)

        # Membuat kotak background krem
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")

        # Insert logo di kiri atas
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.add_question_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        # Insert username di kanan atas
        self.username_text = ttk.Label(self.add_question_frame, text=f"Hi, {self.logged_in_username}",
                                       background="#28003A", foreground="#FFFFFF", font=("Inter", 12 * -1), anchor=tk.E)
        self.username_text.place(x=150.0, y=10.0, width=350.0, height=16.0)

        # Insert teks Select Subject
        self.select_subject_text = ttk.Label(self.add_question_frame, text="Select Subject", background="#D9D9D9", foreground="#000000",
                                        font=("Inter", 12 * -1))
        self.select_subject_text.place(x=214.0, y=100.0)

        # Insert dropdown subject dengan ttk.OptionMenu
        subject_options = ["Mathematics", "Biology"]
        self.subject_dropdown = ttk.OptionMenu(self.add_question_frame, self.subject_chosen, subject_options[0], *subject_options)
        self.subject_dropdown.place(x=196.0, y=118.0, width=120.0, height=20.0)

        # Insert teks Question
        self.question_text = ttk.Label(self.add_question_frame, text="Question", background="#D9D9D9", foreground="#000000",
                                  font=("Inter", 12 * -1))
        self.question_text.place(x=230.0, y=139.0)

        # Insert text box untuk Question
        self.question_entry = Text(self.add_question_frame, foreground="gray", font=("Segoe UI", 10))
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

        # Insert teks Choices
        self.choices_text = ttk.Label(self.add_question_frame, text="Choices (Comma-separated)", background="#D9D9D9", foreground="#000000",
                                 font=("Inter", 12 * -1))
        self.choices_text.place(x=78.0, y=243.0)

        # Insert text box untuk Choices
        self.choice_entry = Text(self.add_question_frame, foreground="gray", font=("Segoe UI", 10))
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

        # Insert teks Correct Answer
        self.correct_answer_text = ttk.Label(self.add_question_frame, text="Correct Answer", background="#D9D9D9", foreground="#000000",
                                        font=("Inter", 12 * -1))
        self.correct_answer_text.place(x=307.0, y=243.0)

        # Insert text box untuk Correct Answer
        self.correct_answer_entry = Text(self.add_question_frame, foreground="gray", font=("Segoe UI", 10))
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

        # ======================================Bagian Add Question Button====================================
        self.add_question_button_image = PhotoImage(file=relative_to_assets("add_question_button.png"))
        self.add_question_button = Button(image=self.add_question_button_image, borderwidth=0, highlightthickness=0,
                                     command=lambda: add_question_callback(), relief="flat")
        self.add_question_button.image = self.add_question_button_image
        self.add_question_button.place(x=188.0, y=316.0, width=135.0, height=22.0)

        def add_question_callback():
            msg = messagebox.showinfo("Notice", "Question successfully added!")
            if msg == "ok":
                # Menampilkan input pertanyaan, choices, dan correct answer
                print(f"Subject: {self.subject_chosen.get()}")
                input_question = self.question_entry.get("1.0", "end-1c")
                print(f"Question: {input_question}")
                input_choice = self.choice_entry.get("1.0", "end-1c")
                print(f"Choices: {input_choice}")
                input_correct_answer = self.correct_answer_entry.get("1.0", "end-1c")
                print(f"Correct Answer: {input_correct_answer}")

                # Kembali ke page add question, bersihkan semua text box
                self.question_entry.delete(0.0, tk.END)
                self.question_entry.insert(0.0, "E.g. What is the value of sine of 90 degrees?")
                self.question_entry.configure(foreground="gray")
                self.choice_entry.delete(0.0, tk.END)
                self.choice_entry.insert(0.0, "E.g. 0,1,-1,2")
                self.choice_entry.configure(foreground="gray")
                self.correct_answer_entry.delete(0.0, tk.END)
                self.correct_answer_entry.insert(0.0, "E.g. 1")
                self.correct_answer_entry.configure(foreground="gray")
                self.add_question_button.focus_set()
        # ====================================================================================================

        # ======================================Bagian Sign Out================================================
        self.sign_out_button_image = PhotoImage(file=relative_to_assets("sign_out_button.png"))
        self.sign_out_button = Button(image=self.sign_out_button_image, borderwidth=0, highlightthickness=0,
                                      command=lambda: sign_out_callback(), relief="flat", cursor="hand2")
        self.sign_out_button.place(x=433.0, y=35.0, width=66.0, height=22.0)

        def sign_out_callback():
            # Ke page sign in
            self.delete_frame()
            self.show_sign_in_page()
        # =====================================================================================================

        # ======================================Bagian Back Button=========================================
        self.back_add_question_button_image = PhotoImage(file=relative_to_assets("back_add_question_button.png"))
        self.back_add_question_button = Button(image=self.back_add_question_button_image, borderwidth=0, highlightthickness=0,
                                          command=lambda: back_button_callback(), relief="flat")
        self.back_add_question_button.image = self.back_add_question_button_image
        self.back_add_question_button.place(x=83.0, y=103.0, width=66.0, height=22.0)

        def back_button_callback():
            # Balik ke role choosing
            self.delete_frame()
            self.role_choosing_page()
        # =====================================================================================================
        self.add_question_frame.place(x=0.0, y=0.0)

    # Fungsi untuk halaman home (student)
    def student_home_page(self):
        # Judul window
        self.window.title("Home (Student)")

        # Membuat Frame
        self.student_home_frame = tk.Frame(self.window, width=512, height=384)

        # Membuat canvas
        self.canvas = Canvas(self.student_home_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)

        # Membuat kotak background krem
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")

        # Insert logo di kiri atas
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.student_home_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        # Insert username di kanan atas
        self.username_text = ttk.Label(self.student_home_frame, text=f"Hi, {self.logged_in_username}",
                                       background="#28003A", foreground="#FFFFFF", font=("Inter", 12 * -1), anchor=tk.E)
        self.username_text.place(x=150.0, y=10.0, width=350.0, height=16.0)

        # =======================================Bagian Take Quiz=========================================
        self.take_quiz_button_image = PhotoImage(file=relative_to_assets("take_quiz_button.png"))
        self.take_quiz_button = Button(image=self.take_quiz_button_image, borderwidth=0, highlightthickness=0,command=lambda:take_quiz_button_callback(), relief="flat")
        self.take_quiz_button.image = self.take_quiz_button_image
        self.take_quiz_button.place(x=188.0, y=141.0, width=135.0, height=22.0)
        def take_quiz_button_callback():
            # Ke halaman pemilihan soal
            self.delete_frame()
            self.quiz_list_page()
        # ================================================================================================

        # =======================================Bagian View History======================================
        self.view_history_button_image = PhotoImage(file=relative_to_assets("view_history_button.png"))
        self.view_history_button = Button(image=self.view_history_button_image, borderwidth=0, highlightthickness=0,command=lambda:view_history_button_callback(), relief="flat")
        self.view_history_button.image = self.view_history_button_image
        self.view_history_button.place(x=188.0, y=192.0, width=135.0, height=22.0)
        def view_history_button_callback():
            # Ke halaman view history
            self.delete_frame()
            self.history_page()
        # ================================================================================================

        # =======================================Bagian Back Button=======================================
        self.back_add_question_button_image = PhotoImage(file=relative_to_assets("back_take_quiz_button.png"))
        self.back_add_question_button = Button(image=self.back_add_question_button_image, borderwidth=0,
                                               highlightthickness=0,
                                               command=lambda: back_button_callback(), relief="flat")
        self.back_add_question_button.image = self.back_add_question_button_image
        self.back_add_question_button.place(x=83.0, y=103.0, width=66.0, height=22.0)

        def back_button_callback():
            # Balik ke role choosing
            self.delete_frame()
            self.role_choosing_page()
        # ================================================================================================

        # =======================================Bagian Sign Out==========================================
        self.sign_out_button_image = PhotoImage(file=relative_to_assets("sign_out_button.png"))
        self.sign_out_button = Button(image=self.sign_out_button_image, borderwidth=0, highlightthickness=0,
                                      command=lambda: sign_out_callback(), relief="flat", cursor="hand2")
        self.sign_out_button.place(x=433.0, y=35.0, width=66.0, height=22.0)

        def sign_out_callback():
            # Ke page sign in
            self.delete_frame()
            self.show_sign_in_page()
        # ================================================================================================

        self.student_home_frame.place(x=0.0, y=0.0)

    # Fungsi untuk halaman history (student)
    def history_page(self):
        # Judul window
        self.window.title("Home (Student)")

        # Membuat Frame
        self.history_frame = tk.Frame(self.window, width=512, height=384)

        # Membuat canvas
        self.canvas = Canvas(self.history_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)

        # Membuat kotak background krem
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")

        # Insert logo di kiri atas
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.history_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        # Insert username di kanan atas
        self.username_text = ttk.Label(self.history_frame, text=f"Hi, {self.logged_in_username}",
                                       background="#28003A", foreground="#FFFFFF", font=("Inter", 12 * -1), anchor=tk.E)
        self.username_text.place(x=150.0, y=10.0, width=350.0, height=16.0)

        # =======================================Bagian Scroll History====================================
        self.history = st.ScrolledText(self.history_frame, font=("Segoe UI", 10))
        self.history.place(x=82.0, y=130.0, width=347.0, height=208.0)
        self.history.insert(tk.INSERT, "Thio\nTriansyah\nPutra\nMuhammad\nRafli\nBagaskara\nSurya\nDharma\n")
        self.history.configure(state='disabled')
        # ================================================================================================

        # =======================================Bagian Back Button=======================================
        self.back_add_question_button_image = PhotoImage(file=relative_to_assets("back_take_quiz_button.png"))
        self.back_add_question_button = Button(image=self.back_add_question_button_image, borderwidth=0,
                                               highlightthickness=0,
                                               command=lambda: back_button_callback(), relief="flat")
        self.back_add_question_button.image = self.back_add_question_button_image
        self.back_add_question_button.place(x=83.0, y=103.0, width=66.0, height=22.0)

        def back_button_callback():
            # Balik ke role choosing
            self.delete_frame()
            self.student_home_page()

        # ================================================================================================

        # =======================================Bagian Sign Out==========================================
        self.sign_out_button_image = PhotoImage(file=relative_to_assets("sign_out_button.png"))
        self.sign_out_button = Button(image=self.sign_out_button_image, borderwidth=0, highlightthickness=0,
                                      command=lambda: sign_out_callback(), relief="flat", cursor="hand2")
        self.sign_out_button.place(x=433.0, y=35.0, width=66.0, height=22.0)

        def sign_out_callback():
            # Ke page sign in
            self.delete_frame()
            self.show_sign_in_page()

        # ================================================================================================

        self.history_frame.place(x=0.0, y=0.0)

    # Fungsi untuk halaman pemilihan soal (student)
    def quiz_list_page(self):
        # Judul window
        self.window.title("Add Question")

        # Membuat Frame
        self.quiz_list_frame = tk.Frame(self.window, width=512, height=384)

        # Membuat canvas
        self.canvas = Canvas(self.quiz_list_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)

        # Membuat kotak background krem
        self.canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")

        # Insert logo di kiri atas
        self.logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
        self.label_image = tk.Label(self.quiz_list_frame, image=self.logo_image, borderwidth=0)
        self.label_image.image = self.logo_image
        self.label_image.place(x=0.0, y=0.0)
        self.canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

        # Insert username di kanan atas
        self.username_text = ttk.Label(self.quiz_list_frame, text=f"Hi, {self.logged_in_username}",
                                       background="#28003A", foreground="#FFFFFF", font=("Inter", 12 * -1), anchor=tk.E)
        self.username_text.place(x=150.0, y=10.0, width=350.0, height=16.0)

        # Insert teks Select Subject
        self.select_subject_text = ttk.Label(self.quiz_list_frame, text="Select Subject", background="#D9D9D9",
                                             foreground="#000000",
                                             font=("Inter", 12 * -1))
        self.select_subject_text.place(x=214.0, y=100.0)

        # Insert dropdown subject dengan ttk.OptionMenu
        subject_options = ["Mathematics", "Biology"]
        self.subject_dropdown = ttk.OptionMenu(self.quiz_list_frame, self.subject_quiz, subject_options[0],*subject_options)
        self.subject_dropdown.place(x=196.0, y=118.0, width=120.0, height=20.0)

        # =======================================Bagian Start Quiz=========================================
        start_quiz_button_image = PhotoImage(file=relative_to_assets("start_quiz_button.png"))
        start_quiz_button = Button(image=start_quiz_button_image, borderwidth=0, highlightthickness=0,command=lambda: start_quiz_button_callback(), relief="flat")
        start_quiz_button.image = start_quiz_button_image
        start_quiz_button.place(x=188.0, y=189.0, width=135.0, height=22.0)

        def start_quiz_button_callback():
            # Ke halaman pengerjaan kuis
            print("Ke halaman pengerjaan kuis")
        # =================================================================================================

        # =======================================Bagian Back Button=======================================
        self.back_add_question_button_image = PhotoImage(file=relative_to_assets("back_start_quiz_button.png"))
        self.back_add_question_button = Button(image=self.back_add_question_button_image, borderwidth=0,
                                               highlightthickness=0,
                                               command=lambda: back_button_callback(), relief="flat")
        self.back_add_question_button.image = self.back_add_question_button_image
        self.back_add_question_button.place(x=83.0, y=103.0, width=66.0, height=22.0)

        def back_button_callback():
            # Balik ke role choosing
            self.delete_frame()
            self.student_home_page()

        # ================================================================================================

        # =======================================Bagian Sign Out==========================================
        self.sign_out_button_image = PhotoImage(file=relative_to_assets("sign_out_button.png"))
        self.sign_out_button = Button(image=self.sign_out_button_image, borderwidth=0, highlightthickness=0,
                                      command=lambda: sign_out_callback(), relief="flat", cursor="hand2")
        self.sign_out_button.place(x=433.0, y=35.0, width=66.0, height=22.0)

        def sign_out_callback():
            # Ke page sign in
            self.delete_frame()
            self.show_sign_in_page()

        # ================================================================================================

        self.quiz_list_frame.place(x=0.0, y=0.0)

    # Fungsi untuk halaman pengerjaan kuis (student)



a = Main_window()