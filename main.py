import random
import string
import secrets
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyperclip
import sqlite3
import os

class PasswordManager:
    def __init__(self):
        self.conn = sqlite3.connect('password_vault.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                length INTEGER,
                level INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def save_password(self, name, password, length, level):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO passwords (name, password, length, level) 
                VALUES (?, ?, ?, ?)
            ''', (name, password, length, level))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not save password: {e}")
            return False

    def retrieve_passwords(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, name, password, length, level FROM passwords')
            return cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not retrieve passwords: {e}")
            return []

    def delete_password(self, password_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not delete password: {e}")
            return False

    def close_connection(self):
        self.conn.close()

def generate_password(level, length, num_digits, num_symbols):
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
   
    if num_symbols + num_digits > length:
        return "Error: The number of symbols and digits exceeds the total password length."
   
    list_symbols = [secrets.choice(symbols) for i in range(num_symbols)]
    list_numbers = [secrets.choice(digits) for i in range(num_digits)]
   
    remaining_length = length - len(list_symbols + list_numbers)
   
    if level == 1:
        password_list = [secrets.choice(letters) for i in range(length)]
    elif level == 2:
        password_list = [secrets.choice(letters) for i in range(remaining_length)] + list_numbers
    elif level == 3:
        password_list = [secrets.choice(letters) for i in range(remaining_length)] + list_numbers + list_symbols
    else:
        return "Invalid choice"
   
    random.shuffle(password_list)
    password = "".join(password_list)
    return password

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.password_manager = PasswordManager()

        self.create_widgets()

    def create_widgets(self):
        length_label = ttk.Label(self.root, text="Password Length:")
        self.length_entry = ttk.Entry(self.root)
        level_label = ttk.Label(self.root, text="Password Level:")
        self.level_combobox = ttk.Combobox(self.root, values=[1, 2, 3], state="readonly")
        num_digits_label = ttk.Label(self.root, text="Number of Digits:")
        self.num_digits_entry = ttk.Entry(self.root)
        num_symbols_label = ttk.Label(self.root, text="Number of Symbols:")
        self.num_symbols_entry = ttk.Entry(self.root)
        
        level_description = ttk.Label(self.root, text="1: Lowercase letters\n2: Lowercase letters and digits\n3: Lowercase letters, digits, and symbols")
        
        generate_button = ttk.Button(self.root, text="Generate Password", command=self.on_generate)
        save_button = ttk.Button(self.root, text="Save Password", command=self.on_save)
        view_button = ttk.Button(self.root, text="View Saved Passwords", command=self.view_passwords)
        
        self.password_label = ttk.Label(self.root, text="Generated password:")
        self.status_label = ttk.Label(self.root, text="")

        length_label.grid(row=0, column=0, padx=10, pady=10)
        self.length_entry.grid(row=0, column=1, padx=10, pady=10)
        level_label.grid(row=1, column=0, padx=10, pady=10)
        self.level_combobox.grid(row=1, column=1, padx=10, pady=10)
        num_digits_label.grid(row=2, column=0, padx=10, pady=10)
        self.num_digits_entry.grid(row=2, column=1, padx=10, pady=10)
        num_symbols_label.grid(row=3, column=0, padx=10, pady=10)
        self.num_symbols_entry.grid(row=3, column=1, padx=10, pady=10)
        level_description.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        generate_button.grid(row=5, column=0, padx=10, pady=10)
        save_button.grid(row=5, column=1, padx=10, pady=10)
        view_button.grid(row=5, column=2, padx=10, pady=10)
        self.password_label.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        self.status_label.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

        self.current_password = None

    def on_generate(self):
        try:
            length = int(self.length_entry.get())
            level = int(self.level_combobox.get())
            num_digits = int(self.num_digits_entry.get())
            num_symbols = int(self.num_symbols_entry.get())
            
            self.current_password = generate_password(level, length, num_digits, num_symbols)
            self.password_label.config(text=f"Generated password: {self.current_password}")
            pyperclip.copy(self.current_password)
            self.status_label.config(text="Password copied to clipboard")
        except ValueError:
            messagebox.showerror("Input Error", "Please fill in all fields with valid numbers")

    def on_save(self):
        if not self.current_password:
            messagebox.showwarning("Save Error", "Generate a password first")
            return

        name = simpledialog.askstring("Save Password", "Enter a name for this password:")
        if name:
            length = int(self.length_entry.get())
            level = int(self.level_combobox.get())
            num_digits = int(self.num_digits_entry.get())
            num_symbols = int(self.num_symbols_entry.get())

            if self.password_manager.save_password(name, self.current_password, length, level):
                messagebox.showinfo("Success", f"Password '{name}' saved successfully")

    def view_passwords(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("Saved Passwords")
        view_window.geometry("600x400")

        columns = ("ID", "Name", "Password", "Length", "Level")
        tree = ttk.Treeview(view_window, columns=columns, show='headings')
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')
        
        passwords = self.password_manager.retrieve_passwords()
        for pwd in passwords:
            tree.insert('', 'end', values=pwd)
        
        scrollbar = ttk.Scrollbar(view_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select a password to delete")
                return
            
            pwd_id = tree.item(selected[0])['values'][0]
            
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this password?"):
                if self.password_manager.delete_password(pwd_id):
                    tree.delete(selected)
                    messagebox.showinfo("Success", "Password deleted")

        delete_button = ttk.Button(view_window, text="Delete Selected", command=delete_selected)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        delete_button.pack(side=tk.BOTTOM, pady=10)

    def on_closing(self):
        self.password_manager.close_connection()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()