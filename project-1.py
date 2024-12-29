#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 23:59:21 2024

@author: hadie
"""
import tkinter as tk
from tkinter import messagebox
import sqlite3

# ------------------- Database Setup -------------------
conn = sqlite3.connect("todo.db")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        status TEXT NOT NULL
    )
""")
conn.commit()

# ------------------- Functions -------------------

def show_main_window():
    login_window.destroy()
    main_window()

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "hadie" and password == "1234":
        show_main_window()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def add_task():
    task = task_entry.get()
    if task:
        cur.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "Pending"))
        conn.commit()
        task_entry.delete(0, tk.END)
        refresh_list()
        messagebox.showinfo("Success", "Task added successfully!")
    else:
        messagebox.showerror("Error", "Please enter a task.")

def delete_task():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_id = task_listbox.get(selected_task).split(".")[0]
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        refresh_list()
        messagebox.showinfo("Success", "Task deleted successfully!")
    else:
        messagebox.showerror("Error", "Please select a task to delete.")

def mark_done():
    selected_task = task_listbox.curselection()
    if selected_task:
        task_id = task_listbox.get(selected_task).split(".")[0]
        cur.execute("UPDATE tasks SET status = ? WHERE id = ?", ("Done", task_id))
        conn.commit()
        refresh_list()
        messagebox.showinfo("Success", "Task marked as completed!")
    else:
        messagebox.showerror("Error", "Please select a task to mark as done.")

def refresh_list():
    task_listbox.delete(0, tk.END)
    cur.execute("SELECT id, task, status FROM tasks")
    tasks = cur.fetchall()
    for task in tasks:
        display_text = f"{task[0]}. {task[1]} [{task[2]}]"
        task_listbox.insert(tk.END, display_text)

def on_closing():
    conn.close()
    window.destroy()

# ------------------- Login Window -------------------

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("400x300")
login_window.configure(bg="#295F98")

# Title Label
login_label = tk.Label(login_window, text="Login", font=("Arial", 24, "bold"), bg="#295F98", fg="#FBFBFB")
login_label.pack(pady=20)

# Username Entry
username_label = tk.Label(login_window, text="Username:", font=("Arial", 14), bg="#295F98", fg="#FBFBFB")
username_label.pack(pady=5)
username_entry = tk.Entry(login_window, font=("Arial", 14), width=30)
username_entry.pack(pady=5)

# Password Entry
password_label = tk.Label(login_window, text="Password:", font=("Arial", 14), bg="#295F98", fg="#FBFBFB")
password_label.pack(pady=5)
password_entry = tk.Entry(login_window, font=("Arial", 14), width=30, show="*")
password_entry.pack(pady=5)

# Login Button
login_button = tk.Button(login_window, text="Login", font=("Arial", 14), bg="#295F98", fg="black", width=15, command=login)
login_button.pack(pady=20)

# ------------------- Main To-Do List Window -------------------

def main_window():
    global window, task_entry, task_listbox

    window = tk.Tk()
    window.title("To-Do List Manager")
    window.geometry("600x500")
    window.configure(bg="#789DBC")
    window.protocol("WM_DELETE_WINDOW", on_closing)

    # Title Label
    title_label = tk.Label(window, text="To-Do List Manager", font=("Arial", 24, "bold"), bg="#B3C8CF", fg="#FBFBFB")
    title_label.pack(pady=20)

    # Task Entry
    task_entry = tk.Entry(window, font=("Arial", 14), width=50)
    task_entry.pack(pady=10)

    # Buttons Frame
    button_frame = tk.Frame(window, bg="#B3C8CF")
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="Add Task", font=("Arial", 12, "bold"), bg="#789DBC", fg="black", width=15, command=add_task)
    add_button.grid(row=0, column=0, padx=10)

    delete_button = tk.Button(button_frame, text="Delete Task", font=("Arial", 12, "bold"), bg="#789DBC", fg="black", width=15, command=delete_task)
    delete_button.grid(row=0, column=1, padx=10)

    done_button = tk.Button(button_frame, text="Mark as Done", font=("Arial", 12, "bold"), bg="#789DBC", fg="black", width=15, command=mark_done)
    done_button.grid(row=0, column=2, padx=10)

    # Task Listbox
    task_listbox = tk.Listbox(window, font=("Arial", 14), width=60, height=15, selectbackground="#E5E1DA")
    task_listbox.pack(pady=10)

    # Load the task list
    refresh_list()

    window.mainloop()

# Start the login window loop
login_window.mainloop()

