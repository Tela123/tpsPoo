import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import datetime


class Livre:
    def __init__(self, titre, auteur, annee, disponible=True):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.disponible = disponible

    def afficher_details(self):
        return f"Titre: {self.titre}, Auteur: {self.auteur}, Année: {self.annee}, Disponible: {'Oui' if self.disponible else 'Non'}"


class Personne:
    def __init__(self, nom, prenom, num_membre):
        self.nom = nom
        self.prenom = prenom
        self.num_membre = num_membre

    def afficher_details(self):
        return f"Nom: {self.nom}, Prénom: {self.prenom}, Numéro de membre: {self.num_membre}"


class Emprunt:
    def __init__(self, id_livre, id_membre, date_emprunt, date_retour_prevue):
        self.id_livre = id_livre
        self.id_membre = id_membre
        self.date_emprunt = date_emprunt
        self.date_retour_prevue = date_retour_prevue


class Bibliotheque:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de gestion de bibliothèque")
        self.root.geometry("800x600")

        # Initialiser la base de données
        self.conn = sqlite3.connect("bibliotheque.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # UI
        self.create_widgets()

    def create_tables(self):
        """Créer les tables nécessaires dans la base de données."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT NOT NULL,
            annee INTEGER NOT NULL,
            disponible BOOLEAN DEFAULT 1
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS membres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            num_membre TEXT NOT NULL UNIQUE
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprunts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livre INTEGER NOT NULL,
            id_membre INTEGER NOT NULL,
            date_emprunt TEXT NOT NULL,
            date_retour_prevue TEXT NOT NULL,
            FOREIGN KEY (id_livre) REFERENCES livres (id),
            FOREIGN KEY (id_membre) REFERENCES membres (id)
        )
        """)
        self.conn.commit()

    def create_widgets(self):
        """Créer les éléments de l'interface utilisateur."""
        # Onglets
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True)

        self.tab_livres = Frame(self.tabs)
        self.tab_membres = Frame(self.tabs)
        self.tab_emprunts = Frame(self.tabs)

        self.tabs.add(self.tab_livres, text="Livres")
        self.tabs.add(self.tab_membres, text="Membres")
        self.tabs.add(self.tab_emprunts, text="Emprunts")

        # Onglet Livres
        self.setup_livres_tab()

        # Onglet Membres
        self.setup_membres_tab()

        # Onglet Emprunts
        self.setup_emprunts_tab()

    def setup_livres_tab(self):
        """Configurer l'onglet Livres."""
        Label(self.tab_livres, text="Titre:").grid(row=0, column=0, padx=10, pady=5)
        self.titre_entry = Entry(self.tab_livres)
        self.titre_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.tab_livres, text="Auteur:").grid(row=1, column=0, padx=10, pady=5)
        self.auteur_entry = Entry(self.tab_livres)
        self.auteur_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.tab_livres, text="Année:").grid(row=2, column=0, padx=10, pady=5)
        self.annee_entry = Entry(self.tab_livres)
        self.annee_entry.grid(row=2, column=1, padx=10, pady=5)

        Button(self.tab_livres, text="Ajouter Livre", command=self.ajouter_livre).grid(row=3, column=1, pady=10)

        self.livres_tree = ttk.Treeview(self.tab_livres, columns=("ID", "Titre", "Auteur", "Année", "Disponible"),
                                        show="headings")
        self.livres_tree.heading("ID", text="ID")
        self.livres_tree.heading("Titre", text="Titre")
        self.livres_tree.heading("Auteur", text="Auteur")
        self.livres_tree.heading("Année", text="Année")
        self.livres_tree.heading("Disponible", text="Disponible")
        self.livres_tree.column("ID", width=50)
        self.livres_tree.grid(row=4, column=0, columnspan=2, pady=10)
        self.load_livres()

    def setup_membres_tab(self):
        """Configurer l'onglet Membres."""
        Label(self.tab_membres, text="Nom:").grid(row=0, column=0, padx=10, pady=5)
        self.nom_entry = Entry(self.tab_membres)
        self.nom_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.tab_membres, text="Prénom:").grid(row=1, column=0, padx=10, pady=5)
        self.prenom_entry = Entry(self.tab_membres)
        self.prenom_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.tab_membres, text="Numéro de membre:").grid(row=2, column=0, padx=10, pady=5)
        self.num_membre_entry = Entry(self.tab_membres)
        self.num_membre_entry.grid(row=2, column=1, padx=10, pady=5)

        Button(self.tab_membres, text="Ajouter Membre", command=self.ajouter_membre).grid(row=3, column=1, pady=10)

        self.membres_tree = ttk.Treeview(self.tab_membres, columns=("ID", "Nom", "Prénom", "Numéro"),
                                         show="headings")
        self.membres_tree.heading("ID", text="ID")
        self.membres_tree.heading("Nom", text="Nom")
        self.membres_tree.heading("Prénom", text="Prénom")
        self.membres_tree.heading("Numéro", text="Numéro")
        self.membres_tree.column("ID", width=50)
        self.membres_tree.grid(row=4, column=0, columnspan=2, pady=10)
        self.load_membres()

    def setup_emprunts_tab(self):
        """Configurer l'onglet Emprunts."""
        # Ajouter les fonctionnalités ici (emprunt et retour)
        pass

    def ajouter_livre(self):
        """Ajouter un livre à la bibliothèque."""
        titre = self.titre_entry.get()
        auteur = self.auteur_entry.get()
        annee = self.annee_entry.get()

        if not titre or not auteur or not annee:
            messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            self.cursor.execute("INSERT INTO livres (titre, auteur, annee) VALUES (?, ?, ?)", (titre, auteur, annee))
            self.conn.commit()
            self.load_livres()
            self.titre_entry.delete(0, END)
            self.auteur_entry.delete(0, END)
            self.annee_entry.delete(0, END)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def load_livres(self):
        """Charger les livres dans l'interface."""
        for row in self.livres_tree.get_children():
            self.livres_tree.delete(row)

        self.cursor.execute("SELECT * FROM livres")
        for row in self.cursor.fetchall():
            disponible = "Oui" if row[4] else "Non"
            self.livres_tree.insert("", END, values=(row[0], row[1], row[2], row[3], disponible))

    def ajouter_membre(self):
        """Ajouter un membre."""
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        num_membre = self.num_membre_entry.get()

        if not nom or not prenom or not num_membre:
            messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
            return
        try:
            self.cursor.execute("INSERT INTO membres (nom, prenom, num_membre) VALUES (?, ?, ?)",
                                (nom, prenom, num_membre))
            self.conn.commit()
            self.load_membres()
            self.nom_entry.delete(0, END)
            self.prenom_entry.delete(0, END)
            self.num_membre_entry.delete(0, END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Le numéro de membre doit être unique.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def load_membres(self):
        """Charger les membres dans l'interface."""
        for row in self.membres_tree.get_children():
            self.membres_tree.delete(row)

        self.cursor.execute("SELECT * FROM membres")
        for row in self.cursor.fetchall():
            self.membres_tree.insert("", END, values=row)
    def setup_emprunts_tab(self):
        """Configurer l'onglet Emprunts."""
        Label(self.tab_emprunts, text="ID Livre:").grid(row=0, column=0, padx=10, pady=5)
        self.id_livre_entry = Entry(self.tab_emprunts)
        self.id_livre_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.tab_emprunts, text="ID Membre:").grid(row=1, column=0, padx=10, pady=5)
        self.id_membre_entry = Entry(self.tab_emprunts)
        self.id_membre_entry.grid(row=1, column=1, padx=10, pady=5)

        Button(self.tab_emprunts, text="Emprunter Livre", command=self.emprunter_livre).grid(row=2, column=1, pady=10)
        Button(self.tab_emprunts, text="Retourner Livre", command=self.retourner_livre).grid(row=3, column=1, pady=10)

        self.emprunts_tree = ttk.Treeview(self.tab_emprunts,
                                          columns=("ID", "Livre", "Membre", "Date Emprunt", "Date Retour Prévue"),
                                          show="headings")
        self.emprunts_tree.heading("ID", text="ID")
        self.emprunts_tree.heading("Livre", text="ID Livre")
        self.emprunts_tree.heading("Membre", text="ID Membre")
        self.emprunts_tree.heading("Date Emprunt", text="Date Emprunt")
        self.emprunts_tree.heading("Date Retour Prévue", text="Date Retour Prévue")
        self.emprunts_tree.column("ID", width=50)
        self.emprunts_tree.grid(row=4, column=0, columnspan=2, pady=10)
        self.load_emprunts()
    def emprunter_livre(self):
        """Permettre à un membre d'emprunter un livre."""
        id_livre = self.id_livre_entry.get()
        id_membre = self.id_membre_entry.get()
        date_emprunt = datetime.date.today().strftime("%Y-%m-%d")
        date_retour_prevue = (datetime.date.today() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")

        if not id_livre or not id_membre:
            messagebox.showwarning("Erreur", "Les champs ID Livre et ID Membre sont obligatoires.")
            return

        try:
            # Vérifier si le livre est disponible
            self.cursor.execute("SELECT disponible FROM livres WHERE id=?", (id_livre,))
            result = self.cursor.fetchone()
            if result is None:
                messagebox.showerror("Erreur", "Livre introuvable.")
                return
            elif not result[0]:
                messagebox.showerror("Erreur", "Ce livre est déjà emprunté.")
                return

            # Ajouter l'emprunt et mettre à jour la disponibilité du livre
            self.cursor.execute("INSERT INTO emprunts (id_livre, id_membre, date_emprunt, date_retour_prevue) VALUES (?, ?, ?, ?)",
                                (id_livre, id_membre, date_emprunt, date_retour_prevue))
            self.cursor.execute("UPDATE livres SET disponible=0 WHERE id=?", (id_livre,))
            self.conn.commit()
            self.load_emprunts()
            self.load_livres()
            self.id_livre_entry.delete(0, END)
            self.id_membre_entry.delete(0, END)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    def retourner_livre(self):
        """Retourner un livre emprunté."""
        selected_item = self.emprunts_tree.selection()
        if not selected_item:
            messagebox.showwarning("Erreur", "Veuillez sélectionner un emprunt à retourner.")
            return

        emprunt_id = self.emprunts_tree.item(selected_item, "values")[0]

        try:
            # Récupérer l'ID du livre associé à l'emprunt
            self.cursor.execute("SELECT id_livre FROM emprunts WHERE id=?", (emprunt_id,))
            id_livre = self.cursor.fetchone()[0]

            # Supprimer l'emprunt et mettre à jour la disponibilité du livre
            self.cursor.execute("DELETE FROM emprunts WHERE id=?", (emprunt_id,))
            self.cursor.execute("UPDATE livres SET disponible=1 WHERE id=?", (id_livre,))
            self.conn.commit()
            self.load_emprunts()
            self.load_livres()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    def load_emprunts(self):
        """Charger les emprunts dans l'interface."""
        for row in self.emprunts_tree.get_children():
            self.emprunts_tree.delete(row)

        self.cursor.execute("""
        SELECT emprunts.id, emprunts.id_livre, emprunts.id_membre, emprunts.date_emprunt, emprunts.date_retour_prevue
        FROM emprunts
        """)
        for row in self.cursor.fetchall():
            self.emprunts_tree.insert("", END, values=row)
if __name__ == "__main__":
    root = Tk()
    app = Bibliotheque(root)
    root.mainloop()