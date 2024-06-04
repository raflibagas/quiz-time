from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
import tkinter as tk
from tkinter import Tk, Canvas, Button, PhotoImage, ttk, messagebox


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Python\PPLJ_GUI\assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("512x384")
window.configure(bg="#FFFFFF")

# Fungsi untuk destroy semua frame
def delete_frame(root):
    for frame in root.winfo_children():
        frame.destroy()

def show_sign_in_page():
    # Judul window
    window.title("Sign In Page")

    # Membuat Frame
    sign_in_frame = tk.Frame(window, width=512, height=384)

    # Membuat canvas
    canvas = Canvas(sign_in_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Membuat kotak background krem
    canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")

    # Insert logo di kiri atas
    logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
    label_image = tk.Label(sign_in_frame, image=logo_image, borderwidth=0)
    label_image.image = logo_image
    label_image.place(x=0.0, y=0.0)
    canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

    # Insert teks judul sign in
    sign_in_title_text = ttk.Label(sign_in_frame, text="Sign In", background="#D9D9D9", foreground="#000000", font=("Inter", 32 * -1))
    sign_in_title_text.place(x=204.0, y=106.0)

    # Insert teks New account?
    new_account_text = ttk.Label(sign_in_frame, text="New account?", background="#D9D9D9", foreground="#000000", font=("Inter", 12 * -1))
    new_account_text.place(x=180.0, y=260.0)

    # Insert teks sign up now, mengarah ke page sign up
    sign_up_text = ttk.Label(sign_in_frame, text="Sign up here", background="#D9D9D9", foreground="#0084FF", font=("Inter", 12 * -1), cursor="hand2")
    sign_up_text.place(x=260.0, y=260.0)

    def to_sign_up_page(event):
        # Ke halaman sign up
        password_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        delete_frame(window)
        show_sign_up_page()

    def bold_sign_up_text(event):
        sign_up_text.configure(font=("Inter", 12 * -1, 'bold'))

    def normalize_sign_up_text(event):
        sign_up_text.configure(font=("Inter", 12 * -1))

    sign_up_text.bind("<Button-1>", to_sign_up_page)
    sign_up_text.bind("<Enter>", bold_sign_up_text)
    sign_up_text.bind("<Leave>", normalize_sign_up_text)

    # ==================================Bagian Entry Password================================
    password_entry = ttk.Entry(sign_in_frame, textvariable=login_password, foreground="gray")
    password_entry.place(x=156.0, y=208.0, width=200.0, height=40.0)
    password_entry.insert(0, "Password")

    def password_in_focus(event):
        if login_password.get() == "Password":
            password_entry.delete(0, tk.END)
            password_entry.configure(foreground="black", show='*')

    def password_out_focus(event):
        if login_password.get() == "":
            password_entry.insert(0, "Password")
            password_entry.configure(foreground="gray", show='')

    password_entry.bind("<FocusIn>", password_in_focus)
    password_entry.bind("<FocusOut>", password_out_focus)
    # ========================================================================================

    # ==================================Bagian Entry Username=================================
    username_entry = ttk.Entry(sign_in_frame, textvariable=login_username, foreground="gray")
    username_entry.place(x=156.0, y=152.0, width=200.0, height=40.0)
    username_entry.insert(0, "Username")

    def username_in_focus(event):
        if login_username.get() == "Username":
            username_entry.delete(0, tk.END)
            username_entry.configure(foreground="black")

    def username_out_focus(event):
        if login_username.get() == "":
            username_entry.insert(0, "Username")
            username_entry.configure(foreground="gray")

    username_entry.bind("<FocusIn>", username_in_focus)
    username_entry.bind("<FocusOut>", username_out_focus)
    # ========================================================================================

    # ==================================Bagian Sign In========================================
    sign_in_button_image = PhotoImage(file=relative_to_assets("sign_in_button.png"))
    sign_in_button = Button(sign_in_frame, image=sign_in_button_image, borderwidth=0, highlightthickness=0, command=lambda: sign_in_callback(), relief="flat", cursor="hand2")
    sign_in_button.image = sign_in_button_image
    sign_in_button.place(x=156.0, y=285.0, width=200.0, height=40.0)

    def sign_in_callback():
        if login_username.get() == "Username" or login_password.get() == "Password":
            msg = messagebox.showinfo("Notice", "Username or Password empty or invalid!")
        else:
            msg = messagebox.showinfo("Notice", "Signed in!\nPress OK to continue")
            # if msg == "ok":
            # masuk ke halaman pilih role (client)
    # ========================================================================================
    sign_in_frame.place(x=0, y=0)

def show_sign_up_page():
    # Judul window
    window.title("Sign Up Page")

    # Membuat Frame
    sign_up_frame = tk.Frame(window, width=512, height=384)

    # Membuat canvas
    canvas = Canvas(sign_up_frame, bg="#FFFFFF", height=384, width=512, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Membuat kotak background krem
    canvas.create_rectangle(78.0, 97.0, 433.0, 347.0, fill="#D9D9D9", outline="")

    # Insert logo di kiri atas
    logo_image = PhotoImage(file=relative_to_assets("app_logo.png"))
    label_image = tk.Label(sign_up_frame, image=logo_image, borderwidth=0)
    label_image.image = logo_image
    label_image.place(x=0.0, y=0.0)
    canvas.create_rectangle(125.0, 0.0, 512.0, 67.0, fill="#28003A", outline="")

    # Insert teks judul sign up
    sign_up_title_text = ttk.Label(sign_up_frame, text="Sign Up", background="#D9D9D9", foreground="#000000", font=("Inter", 32 * -1))
    sign_up_title_text.place(x=204.0, y=106.0)

    # Insert teks have an account?
    new_account_text = ttk.Label(sign_up_frame, text="Have an account?", background="#D9D9D9", foreground="#000000", font=("Inter", 12 * -1))
    new_account_text.place(x=168.0, y=260.0)

    # Insert teks sign in now, mengarah ke page sign in
    sign_in_text = ttk.Label(sign_up_frame, text="Sign in here", background="#D9D9D9", foreground="#0084FF", font=("Inter", 12 * -1), cursor="hand2")
    sign_in_text.place(x=270.0, y=260.0)

    def to_sign_in_page(event):
        # Ke halaman sign in
        password_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        delete_frame(window)
        show_sign_in_page()

    def bold_sign_in_text(event):
        sign_in_text.configure(font=("Inter", 12 * -1, 'bold'))

    def normalize_sign_in_text(event):
        sign_in_text.configure(font=("Inter", 12 * -1))

    sign_in_text.bind("<Button-1>", to_sign_in_page)
    sign_in_text.bind("<Enter>", bold_sign_in_text)
    sign_in_text.bind("<Leave>", normalize_sign_in_text)

    # ==================================Bagian Entry Password================================
    password_entry = ttk.Entry(sign_up_frame, textvariable=register_password, foreground="gray")
    password_entry.place(x=156.0, y=208.0, width=200.0, height=40.0)
    password_entry.insert(0, "Password")

    def password_in_focus(event):
        if register_password.get() == "Password":
            password_entry.delete(0, tk.END)
            password_entry.configure(foreground="black", show='*')

    def password_out_focus(event):
        if register_password.get() == "":
            password_entry.insert(0, "Password")
            password_entry.configure(foreground="gray", show='')

    password_entry.bind("<FocusIn>", password_in_focus)
    password_entry.bind("<FocusOut>", password_out_focus)
    # ========================================================================================

    # ==================================Bagian Entry Username=================================
    username_entry = ttk.Entry(sign_up_frame, textvariable=register_username, foreground="gray")
    username_entry.place(x=156.0, y=152.0, width=200.0, height=40.0)
    username_entry.insert(0, "Username")

    def username_in_focus(event):
        if register_username.get() == "Username":
            username_entry.delete(0, tk.END)
            username_entry.configure(foreground="black")

    def username_out_focus(event):
        if register_username.get() == "":
            username_entry.insert(0, "Username")
            username_entry.configure(foreground="gray")

    username_entry.bind("<FocusIn>", username_in_focus)
    username_entry.bind("<FocusOut>", username_out_focus)
    # ========================================================================================

    # ==================================Bagian Sign In========================================
    register_button_image = PhotoImage(file=relative_to_assets("register_button.png"))
    register_button = Button(sign_up_frame, image=register_button_image, borderwidth=0, highlightthickness=0, command=lambda: sign_in_callback(), relief="flat", cursor="hand2")
    register_button.image = register_button_image
    register_button.place(x=156.0, y=285.0, width=200.0, height=40.0)

    def sign_in_callback():
        if register_username.get() == "Username" or register_password.get() == "Password":
            msg = messagebox.showinfo("Notice", "Username or Password empty or invalid!")
        else:
            msg = messagebox.showinfo("Notice", "Registered!\nPress OK to continue")
            if msg == "ok":
                # Masuk ke halaman sign in
                password_entry.delete(0, tk.END)
                username_entry.delete(0, tk.END)
                delete_frame(window)
                show_sign_in_page()
    # ========================================================================================
    sign_up_frame.place(x=0, y=0)

login_username = tk.StringVar()
login_password = tk.StringVar()
register_username = tk.StringVar()
register_password = tk.StringVar()

show_sign_in_page()

window.resizable(False, False)
window.mainloop()
