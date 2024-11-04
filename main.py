import random
import string
import secrets
import tkinter as tk
from tkinter import ttk
import pyperclip

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

def on_generate():
    length = int(length_entry.get())
    level = int(level_combobox.get())
    num_digits = int(num_digits_entry.get())
    num_symbols = int(num_symbols_entry.get())
    password = generate_password(level, length, num_digits, num_symbols)
    password_label.config(text=f"Generated password: {password}")
    pyperclip.copy(password)
    status_label.config(text="Password copied to clipboard")

root = tk.Tk()
root.title("Password Generator")

# Create the GUI elements
length_label = ttk.Label(root, text="Password Length:")
length_entry = ttk.Entry(root)

level_label = ttk.Label(root, text="Password Level:")
level_combobox = ttk.Combobox(root, values=[1, 2, 3], state="readonly")

num_digits_label = ttk.Label(root, text="Number of Digits:")
num_digits_entry = ttk.Entry(root)

num_symbols_label = ttk.Label(root, text="Number of Symbols:")
num_symbols_entry = ttk.Entry(root)

level_description = ttk.Label(root, text="1: Lowercase letters\n2: Lowercase letters and digits\n3: Lowercase letters, digits, and symbols")

generate_button = ttk.Button(root, text="Generate Password", command=on_generate)
password_label = ttk.Label(root, text="Generated password:")
status_label = ttk.Label(root, text="")

# Grid layout
length_label.grid(row=0, column=0, padx=10, pady=10)
length_entry.grid(row=0, column=1, padx=10, pady=10)

level_label.grid(row=1, column=0, padx=10, pady=10)
level_combobox.grid(row=1, column=1, padx=10, pady=10)

num_digits_label.grid(row=2, column=0, padx=10, pady=10)
num_digits_entry.grid(row=2, column=1, padx=10, pady=10)

num_symbols_label.grid(row=3, column=0, padx=10, pady=10)
num_symbols_entry.grid(row=3, column=1, padx=10, pady=10)

level_description.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

generate_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
password_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
status_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
