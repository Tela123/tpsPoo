import tkinter as tk

def calculate():
    try:
        result = eval(entry.get())
        label_result.config(text=f"Résultat : {result}")
    except Exception:
        label_result.config(text="Erreur")

root = tk.Tk()
root.title("Calculatrice Basique")

entry = tk.Entry(root, width=20, font=("Arial", 16), bg="gray")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+"
]

row_val = 1
col_val = 0

for button in buttons:
    def cmd(x=button):
        if x == "=":
            calculate()
        else:
            entry.insert(tk.END, x)
    tk.Button(root, text=button, width=5, height=2, command=cmd).grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

label_result = tk.Label(root, text="Résultat : ", font=("Arial", 14), bg="silver")
label_result.grid(row=row_val, column=0, columnspan=4, pady=10)

root.mainloop()