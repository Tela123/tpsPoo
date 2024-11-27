import tkinter as tk

def validate():
    prenom = entry_prenom.get()
    nom = entry_nom.get()
    ville = entry_ville.get()
    label_result.config(text=f"{prenom} / {nom} / {ville}")

def reset():
    entry_prenom.delete(0, tk.END)
    entry_nom.delete(0, tk.END)
    entry_ville.delete(0, tk.END)
    label_result.config(text="")

root = tk.Tk()
root.title("Formulaire")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Votre prénom :").grid(row=0, column=0, padx=5, pady=5)
entry_prenom = tk.Entry(frame, width=20)
entry_prenom.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Votre nom :").grid(row=1, column=0, padx=5, pady=5)
entry_nom = tk.Entry(frame, width=20)
entry_nom.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Votre ville :").grid(row=2, column=0, padx=5, pady=5)
entry_ville = tk.Entry(frame, width=20)
entry_ville.grid(row=2, column=1, padx=5, pady=5)

btn_validate = tk.Button(frame, text="Valider", command=validate)
btn_validate.grid(row=3, column=0, padx=5, pady=5)

btn_reset = tk.Button(frame, text="Réinitialiser", command=reset)
btn_reset.grid(row=3, column=1, padx=5, pady=5)

label_result = tk.Label(root, text="", font=("Arial", 14))
label_result.pack(pady=10)

btn_quit = tk.Button(root, text="Quitter", command=root.destroy)
btn_quit.pack(pady=5)

root.mainloop()