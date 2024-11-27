import tkinter as tk
from tkinter import messagebox
import hashlib
import sqlite3


# Exceptions personnalisées
class AuthException(Exception):
    pass


class UserNotFound(AuthException):
    pass


class PasswordIncorrect(AuthException):
    pass


class UserAlreadyExists(AuthException):
    pass


class NotAuthorized(AuthException):
    pass


# Authenticator
class Authenticator:
    def __init__(self, db_path="auth.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS permissions (
                permission TEXT PRIMARY KEY
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_permissions (
                username TEXT,
                permission TEXT,
                FOREIGN KEY (username) REFERENCES users(username),
                FOREIGN KEY (permission) REFERENCES permissions(permission),
                PRIMARY KEY (username, permission)
            )
        """)
        conn.commit()
        conn.close()

    def add_user(self, username, password):
        password_hash = self._hash_password(password)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            raise UserAlreadyExists(f"User '{username}' already exists.")
        finally:
            conn.close()

    def login(self, username, password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        if not result:
            raise UserNotFound(f"User '{username}' not found.")
        if result[0] != self._hash_password(password):
            raise PasswordIncorrect("Incorrect password.")
        return True

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


# Authorizor
class Authorizor:
    def __init__(self, db_path="auth.db"):
        self.db_path = db_path

    def add_permission(self, permission):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO permissions (permission) VALUES (?)", (permission,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # Permission already exists
        finally:
            conn.close()

    def grant_permission(self, username, permission):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO user_permissions (username, permission) VALUES (?, ?)", (username, permission))
            conn.commit()
        except sqlite3.IntegrityError:
            raise NotAuthorized(f"User '{username}' already has permission '{permission}' or does not exist.")
        finally:
            conn.close()

    def check_permission(self, username, permission):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM user_permissions WHERE username = ? AND permission = ?", (username, permission))
        result = cursor.fetchone()
        conn.close()
        if not result:
            raise NotAuthorized(f"User '{username}' is not authorized for '{permission}'.")
        return True


# Interface Tkinter
class AuthApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.authenticator = Authenticator()
        self.authorizor = Authorizor()

        self.title("Système d'authentification")
        self.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.label_username = tk.Label(self, text="Nom d'utilisateur")
        self.label_username.pack()
        self.entry_username = tk.Entry(self)
        self.entry_username.pack()

        self.label_password = tk.Label(self, text="Mot de passe")
        self.label_password.pack()
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack()

        self.btn_register = tk.Button(self, text="Créer un utilisateur", command=self.register_user)
        self.btn_register.pack()

        self.btn_login = tk.Button(self, text="Se connecter", command=self.login_user)
        self.btn_login.pack()

        self.label_permission = tk.Label(self, text="Permission")
        self.label_permission.pack()
        self.entry_permission = tk.Entry(self)
        self.entry_permission.pack()

        self.btn_grant_permission = tk.Button(self, text="Attribuer une permission", command=self.grant_permission)
        self.btn_grant_permission.pack()

        self.btn_check_permission = tk.Button(self, text="Vérifier une permission", command=self.check_permission)
        self.btn_check_permission.pack()

    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        try:
            self.authenticator.add_user(username, password)
            messagebox.showinfo("Succès", f"Utilisateur '{username}' ajouté.")
        except UserAlreadyExists as e:
            messagebox.showerror("Erreur", str(e))

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        try:
            self.authenticator.login(username, password)
            messagebox.showinfo("Succès", f"Bienvenue, {username} !")
        except (UserNotFound, PasswordIncorrect) as e:
            messagebox.showerror("Erreur", str(e))

    def grant_permission(self):
        username = self.entry_username.get()
        permission = self.entry_permission.get()
        try:
            self.authorizor.grant_permission(username, permission)
            messagebox.showinfo("Succès", f"Permission '{permission}' attribuée à '{username}'.")
        except NotAuthorized as e:
            messagebox.showerror("Erreur", str(e))

    def check_permission(self):
        username = self.entry_username.get()
        permission = self.entry_permission.get()
        try:
            self.authorizor.check_permission(username, permission)
            messagebox.showinfo("Succès", f"L'utilisateur '{username}' est autorisé pour '{permission}'.")
        except NotAuthorized as e:
            messagebox.showerror("Erreur", str(e))


if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()