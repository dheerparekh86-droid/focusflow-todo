import tkinter as tk
from tkinter import messagebox

FILE_NAME = "tasks.txt"

# ---------------- COLORS & STYLES ---------------- #
BG_COLOR = "#0f172a"       # Dark blue
CARD_COLOR = "#1e293b"     # Card background
ACCENT = "#38bdf8"         # Blue accent
SUCCESS = "#22c55e"        # Green
TEXT_COLOR = "#e5e7eb"     # Light text
MUTED_TEXT = "#94a3b8"

FONT_MAIN = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI", 20, "bold")

# ---------------- FILE HANDLING ---------------- #

def load_tasks():
    task_list = []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                if "|" in line:
                    task, status = line.strip().split("|")
                    task_list.append([task, int(status)])
    except FileNotFoundError:
        pass
    return task_list


def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        for task, status in tasks:
            file.write(f"{task}|{status}\n")

# ---------------- CORE FUNCTIONS ---------------- #

def add_task():
    task = task_entry.get().strip()
    if not task:
        messagebox.showwarning("Empty Task", "Please enter a task.")
        return

    tasks.append([task, 0])
    save_tasks()
    update_listbox()
    task_entry.delete(0, tk.END)


def delete_task():
    try:
        index = task_listbox.curselection()[0]
        tasks.pop(index)
        save_tasks()
        update_listbox()
    except IndexError:
        messagebox.showwarning("No Selection", "Select a task to delete.")


def mark_completed():
    try:
        index = task_listbox.curselection()[0]
        tasks[index][1] = 1
        save_tasks()
        update_listbox()
    except IndexError:
        messagebox.showwarning("No Selection", "Select a task to complete.")


def update_listbox():
    task_listbox.delete(0, tk.END)
    for task, status in tasks:
        if status == 1:
            task_listbox.insert(tk.END, f"✔  {task}")
        else:
            task_listbox.insert(tk.END, f"•  {task}")

# ---------------- GUI SETUP ---------------- #

root = tk.Tk()
root.title("FocusFlow • To-Do")
root.geometry("460x550")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# ---------------- HEADER ---------------- #

header = tk.Frame(root, bg=BG_COLOR)
header.pack(pady=20)

title = tk.Label(
    header,
    text="FocusFlow",
    font=FONT_TITLE,
    fg=ACCENT,
    bg=BG_COLOR
)
title.pack()

subtitle = tk.Label(
    header,
    text="Stay focused. Get things done.",
    font=FONT_MAIN,
    fg=MUTED_TEXT,
    bg=BG_COLOR
)
subtitle.pack()

# ---------------- CARD ---------------- #

card = tk.Frame(root, bg=CARD_COLOR, padx=15, pady=15)
card.pack(padx=20, pady=10, fill="both", expand=True)

# Entry
task_entry = tk.Entry(
    card,
    font=FONT_MAIN,
    bg="#020617",
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat"
)
task_entry.pack(fill="x", pady=(0, 10))
task_entry.focus()

# Buttons
btn_frame = tk.Frame(card, bg=CARD_COLOR)
btn_frame.pack(pady=5)

def styled_button(text, command, color):
    return tk.Button(
        btn_frame,
        text=text,
        command=command,
        font=FONT_MAIN,
        bg=color,
        fg="#020617",
        activebackground=color,
        relief="flat",
        padx=10,
        pady=5,
        cursor="hand2"
    )

styled_button("Add", add_task, ACCENT).grid(row=0, column=0, padx=5)
styled_button("Done", mark_completed, SUCCESS).grid(row=0, column=1, padx=5)
styled_button("Delete", delete_task, "#f87171").grid(row=0, column=2, padx=5)

# ---------------- LISTBOX + SCROLL ---------------- #

list_frame = tk.Frame(card, bg=CARD_COLOR)
list_frame.pack(fill="both", expand=True, pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

task_listbox = tk.Listbox(
    list_frame,
    font=FONT_MAIN,
    bg="#020617",
    fg=TEXT_COLOR,
    selectbackground=ACCENT,
    selectforeground="#020617",
    relief="flat",
    yscrollcommand=scrollbar.set
)
task_listbox.pack(fill="both", expand=True)
scrollbar.config(command=task_listbox.yview)

# ---------------- LOAD TASKS ---------------- #

tasks = load_tasks()
update_listbox()

root.mainloop()
