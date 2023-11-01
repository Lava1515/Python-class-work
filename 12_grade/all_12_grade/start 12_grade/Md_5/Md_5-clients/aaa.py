import tkinter as tk
from tkinter import ttk
def update_progress_bar(current_value):
    if current_value <= 100:
        progress_var.set(current_value)
        current_value += 1
        root.after(1000, update_progress_bar, current_value)

root = tk.Tk()
root.title("Progress Bar Example")

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(padx=20, pady=20, fill=tk.X)

update_progress_bar(0)

root.mainloop()
