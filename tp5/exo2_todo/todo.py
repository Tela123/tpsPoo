import tkinter as tk
from tkinter import messagebox

def add_task():
    task = entry_task.get()
    if task:
        listbox_tasks.insert(tk.END, task)
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Avertissement", "Veuillez entrer une tâche.")

def delete_task():
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(selected_task_index)
    except IndexError:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner une tâche à supprimer.")

def complete_task():
    try:
        selected_task_index = listbox_tasks.curselection()[0]
        task = listbox_tasks.get(selected_task_index)
        listbox_tasks.delete(selected_task_index)
        listbox_tasks.insert(tk.END, f"{task} (Terminé)")
    except IndexError:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner une tâche.")

root = tk.Tk()
root.title("ToDo List")

frame = tk.Frame(root)
frame.pack(pady=10)

entry_task = tk.Entry(frame, width=30)
entry_task.pack(side=tk.LEFT, padx=5)

btn_add = tk.Button(frame, text="Ajouter", command=add_task)
btn_add.pack(side=tk.LEFT)

listbox_tasks = tk.Listbox(root, width=50, height=10)
listbox_tasks.pack(pady=10)

btn_complete = tk.Button(root, text="Marquer comme Terminé", command=complete_task)
btn_complete.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(root, text="Supprimer", command=delete_task)
btn_delete.pack(side=tk.LEFT, padx=5)

root.mainloop()