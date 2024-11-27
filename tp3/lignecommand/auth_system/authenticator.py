import hashlib
from database import execute_query, fetch_query
from exceptions import UserAlreadyExists, UserNotFound

class Authenticator:
    @staticmethod
    def add_user(username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            execute_query(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
        except sqlite3.IntegrityError:
            raise UserAlreadyExists("L'utilisateur existe déjà.")

    @staticmethod
    def authenticate(username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        result = fetch_query(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        if not result:
            raise UserNotFound("Nom d'utilisateur ou mot de passe incorrect.")
        return result[0][0]  # Retourne l'ID de l'utilisateur