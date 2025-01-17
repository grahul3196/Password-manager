import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import os
import random
import string

class PasswordManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        self.create_gui()

    def load_key(self):
        if os.path.exists("secret.key"):
            with open("secret.key", "rb") as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open("secret.key", "wb") as key_file:
                key_file.write(key)
        return key

    def create_gui(self):
        self.master.geometry("400x400")
        self.master.resizable(False, False)
        self.master.configure(bg="#ADD8E6")

        style = ttk.Style()
        style.configure("TLabel", font=("new times roman", 12), foreground="#ECF0F1")
        style.configure("TButton", font=("new times roman", 12), foreground="#000000")
        style.configure("TEntry", font=("new times roman", 12))

        self.label = ttk.Label(self.master, text="Digital Locker", font=("Garamond", 20, "bold"), foreground="#000000" )
        self.label.pack(pady=10)

        self.service_label = ttk.Label(self.master, text="Service:", background="#000000")
        self.service_label.pack(pady=5)
        self.service_entry = ttk.Entry(self.master)
        self.service_entry.pack(pady=5)

        self.username_label = ttk.Label(self.master, text="Username:", background="#000000")
        self.username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self.master)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(self.master, text="Password:", background="#000000")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.master, show="*")
        self.password_entry.pack(pady=5)

        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(self.master, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility)
        self.show_password_check.pack(pady=5)

        self.generate_button = ttk.Button(self.master, text="Create Password", command=self.generate_password)
        self.generate_button.pack(pady=5)

        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=10)

        self.save_button = ttk.Button(self.button_frame, text="Save", command=self.save_password)
        self.save_button.grid(row=0, column=0, padx=5, pady=5)

        self.retrieve_button = ttk.Button(self.button_frame, text="Get password", command=self.retrieve_password)
        self.retrieve_button.grid(row=0, column=1, padx=5, pady=5)

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def generate_password(self):
        length = 12
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def save_password(self):
        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if service and username and password:
            encrypted_password = self.cipher.encrypt(password.encode())
            with open(f"{service}.txt", "wb") as file:
                file.write(username.encode() + b"\n" + encrypted_password)
            messagebox.showinfo("Success", " yeah! I kept your secret!")
            self.clear_entries()
        else:
            messagebox.showwarning("Error", "Please fill in all fields.")

    def retrieve_password(self):
        service = self.service_entry.get()

        if service:
            try:
                with open(f"{service}.txt", "rb") as file:
                    username = file.readline().strip().decode()
                    encrypted_password = file.readline().strip()
                    password = self.cipher.decrypt(encrypted_password).decode()
                messagebox.showinfo("Password Retrieved", f"Username: {username}\nPassword: {password}")
            except FileNotFoundError:
                messagebox.showwarning("Error", "No password found for this service.")
        else:
            messagebox.showwarning("Error", "Please enter the service name.")

    def clear_entries(self):
        self.service_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
