from tkinter import messagebox as ms
import sqlite3
from PIL import ImageTk, Image
import tkinter as tk
import subprocess
from session import current_user

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.build_widgets()

    def login(self):
        current_user = self.email.get()

        with sqlite3.connect('evaluation.db') as db:
            c = db.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS registration (
                    Fullname TEXT, address TEXT, username TEXT, Email TEXT,
                    Phoneno TEXT, Gender TEXT, age TEXT, password TEXT
                )
            """)
            db.commit()

            c.execute("SELECT * FROM registration WHERE Email = ? AND password = ?",
                      (self.email.get(), self.password.get()))
            result = c.fetchone()

        if result:
            ms.showinfo("Success", "Logged in successfully!")
        else:
            ms.showerror("Oops!", "Email or password did not match.")

        # 🚀 Redirect no matter what
        subprocess.Popen(["python", "GUI_Master.py"])

    def build_widgets(self):
        self.head = tk.Label(self.master, text='Welcome To Login', bg="black", fg="white",
                             font=('Times New Roman', 20, "bold"), pady=10)
        self.head.pack()

        self.logf = tk.Frame(self.master, bg="#154472")

        tk.Label(self.logf, text='Email:', bg="white", fg="black", font=("Times New Roman", 20)).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=10)
        tk.Entry(self.logf, textvariable=self.email, bd=5, bg="white", fg="black", font=('', 15)).grid(
            row=0, column=1, padx=10, pady=10)

        tk.Label(self.logf, text='Password:', bg="white", fg="black", font=("Times New Roman", 20)).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10)
        tk.Entry(self.logf, textvariable=self.password, bd=5, bg="white", fg="black", font=('', 15), show='*').grid(
            row=1, column=1, padx=10, pady=10)

        tk.Button(self.logf,
                  text=' Login ',
                  command=self.login,
                  bd=2,
                  font=("Times New Roman", 20, "bold"),
                  bg="black",
                  fg="white",
                  activebackground="black",
                  activeforeground="white",
                  highlightbackground="black",
                  padx=10,
                  pady=5,
                  relief="raised",
                  cursor="hand2"
                  ).grid(row=2, column=1, pady=10)

        self.logf.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.4)

# ======================================
# Main root setup
root = tk.Tk()
root.title("Login")
root.geometry("800x600")

# Background Image Setup
bg_img = Image.open('B1.jpg').resize((800, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

LoginApp(root)
root.mainloop()
