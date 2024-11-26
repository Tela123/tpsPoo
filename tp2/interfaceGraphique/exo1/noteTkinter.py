import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import datetime


class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carnet de Notes")
        self.root.geometry("600x400")
        
        # Initialize database
        self.conn = sqlite3.connect("notes.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        
        # UI Elements
        self.create_widgets()
        self.load_notes()
    
    def create_table(self):
        """Créer une table pour stocker les notes."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memo TEXT NOT NULL,
            tags TEXT,
            date TEXT NOT NULL
        )
        """)
        self.conn.commit()
    
    def create_widgets(self):
        """Créer les éléments de l'interface."""
        # Input fields
        Label(self.root, text="Mémo:").grid(row=0, column=0, padx=10, pady=10, sticky=E)
        self.memo_entry = Entry(self.root, width=50)
        self.memo_entry.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        
        Label(self.root, text="Balises:").grid(row=1, column=0, padx=10, pady=10, sticky=E)
        self.tags_entry = Entry(self.root, width=50)
        self.tags_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        
        # Buttons
        Button(self.root, text="Ajouter une note", command=self.add_note).grid(row=2, column=1, pady=10, sticky=W)
        Button(self.root, text="Rechercher", command=self.search_notes).grid(row=2, column=1, pady=10, sticky=E)
        
        # Note List
        self.note_tree = ttk.Treeview(self.root, columns=("ID", "Mémo", "Balises", "Date"), show="headings")
        self.note_tree.heading("ID", text="ID")
        self.note_tree.heading("Mémo", text="Mémo")
        self.note_tree.heading("Balises", text="Balises")
        self.note_tree.heading("Date", text="Date")
        self.note_tree.column("ID", width=50)
        self.note_tree.column("Mémo", width=200)
        self.note_tree.column("Balises", width=100)
        self.note_tree.column("Date", width=100)
        self.note_tree.grid(row=3, column=0, columnspan=2, pady=20)
        self.note_tree.bind("<Double-1>", self.edit_note)
    
    def add_note(self):
        """Ajouter une nouvelle note."""
        memo = self.memo_entry.get().strip()
        tags = self.tags_entry.get().strip()
        date = datetime.date.today().strftime("%Y-%m-%d")
        
        if not memo:
            messagebox.showwarning("Attention", "Le mémo ne peut pas être vide.")
            return
        
        self.cursor.execute("INSERT INTO notes (memo, tags, date) VALUES (?, ?, ?)", (memo, tags, date))
        self.conn.commit()
        self.load_notes()
        self.memo_entry.delete(0, END)
        self.tags_entry.delete(0, END)
    
    def load_notes(self):
        """Charger et afficher les notes."""
        for row in self.note_tree.get_children():
            self.note_tree.delete(row)
        
        self.cursor.execute("SELECT * FROM notes")
        for row in self.cursor.fetchall():
            self.note_tree.insert("", END, values=row)
    
    def search_notes(self):
        """Rechercher des notes."""
        query = self.memo_entry.get().strip()
        for row in self.note_tree.get_children():
            self.note_tree.delete(row)
        
        self.cursor.execute("SELECT * FROM notes WHERE memo LIKE ? OR tags LIKE ?", (f"%{query}%", f"%{query}%"))
        for row in self.cursor.fetchall():
            self.note_tree.insert("", END, values=row)
    
    def edit_note(self, event):
        """Modifier une note existante en double cliquant dessus."""
        selected_item = self.note_tree.selection()
        if not selected_item:
            return
        
        note_id = self.note_tree.item(selected_item, "values")[0]
        self.cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
        note = self.cursor.fetchone()
        
        def save_changes():
            memo = memo_entry.get().strip()
            tags = tags_entry.get().strip()
            if not memo:
                messagebox.showwarning("Attention", "Le mémo ne peut pas être vide.")
                return
            self.cursor.execute("UPDATE notes SET memo=?, tags=? WHERE id=?", (memo, tags, note_id))
            self.conn.commit()
            self.load_notes()
            edit_window.destroy()
        
        # Fenêtre de modification
        edit_window = Toplevel(self.root)
        edit_window.title("Modifier la note")
        Label(edit_window, text="Mémo:").grid(row=0, column=0, padx=10, pady=10)
        memo_entry = Entry(edit_window, width=50)
        memo_entry.grid(row=0, column=1, padx=10, pady=10)
        memo_entry.insert(0, note[1])
        
        Label(edit_window, text="Balises:").grid(row=1, column=0, padx=10, pady=10)
        tags_entry = Entry(edit_window, width=50)
        tags_entry.grid(row=1, column=1, padx=10, pady=10)
        tags_entry.insert(0, note[2])
        
        Button(edit_window, text="Sauvegarder", command=save_changes).grid(row=2, column=1, pady=10, sticky=E)
    
    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    root = Tk()
    app = NoteApp(root)
    root.mainloop()