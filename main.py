import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import string
import json
import pyperclip

HIST_FILE = "history.json"
MIN_LEN, MAX_LEN = 6, 32

def load_history():
    try:
        with open(HIST_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    with open(HIST_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def generate_password():
    length = int(scale_len.get())
    use_letters = var_letters.get()
    use_digits = var_digits.get()
    use_symbols = var_symbols.get()
    
    if not (use_letters or use_digits or use_symbols):
        messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
        return

    chars = ''
    if use_letters: chars += string.ascii_letters
    if use_digits: chars += string.digits
    if use_symbols: chars += string.punctuation

    password = ''.join(random.choices(chars, k=length))
    history.append(password)
    save_history(history)
    update_treeview()
    return password

def update_treeview():
    for i in tree.get_children(): tree.delete(i)
    for i, pwd in enumerate(history[-10:], 1):
        tree.insert("", "end", values=(i, pwd))

def on_copy(event):
    item = tree.selection()
    if item:
        pwd = tree.item(item)['values'][1]
        pyperclip.copy(pwd)
        messagebox.showinfo("Копирование", "Пароль скопирован!")

# --- GUI ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x400")
root.resizable(False, False)

history = load_history()

# Длина пароля
tk.Label(root, text="Длина пароля:").pack(pady=5)
scale_len = tk.Scale(root, from_=MIN_LEN, to=MAX_LEN, orient=tk.HORIZONTAL, length=300)
scale_len.set(12)
scale_len.pack()

# Типы символов
frame = tk.Frame(root)
frame.pack(pady=10)
var_letters = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)
tk.Checkbutton(frame, text="Буквы", variable=var_letters).grid(row=0, column=0, padx=5)
tk.Checkbutton(frame, text="Цифры", variable=var_digits).grid(row=0, column=1, padx=5)
tk.Checkbutton(frame, text="Спецсимволы", variable=var_symbols).grid(row=0, column=2, padx=5)

# Кнопка генерации
tk.Button(root, text="Сгенерировать", command=generate_password).pack(pady=10)

# Таблица истории
tree = ttk.Treeview(root, columns=("id", "password"), show="headings")
tree.heading("id", text="№")
tree.heading("password", text="Пароль")
tree.column("password", minwidth=200, width=300)
tree.pack(expand=True, fill='both')
tree.bind("<Double-1>", on_copy)
update_treeview()

root.mainloop()
