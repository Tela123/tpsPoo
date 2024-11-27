from database import execute_query, fetch_query
from exceptions import (
    PermissionAlreadyExists, PermissionNotFound, UserPermissionError
)

class Authorizor:
    @staticmethod
    def add_permission(permission):
        try:
            execute_query(
                "INSERT INTO permissions (permission) VALUES (?)",
                (permission,)
            )
        except sqlite3.IntegrityError:
            raise PermissionAlreadyExists("La permission existe déjà.")

    @staticmethod
    def assign_permission(username, permission):
        # Récupérer l'ID de l'utilisateur
        user = fetch_query("SELECT id FROM users WHERE username = ?", (username,))
        if not user:
            raise UserNotFound("Utilisateur introuvable.")
        user_id = user[0][0]

        # Récupérer l'ID de la permission
        perm = fetch_query("SELECT id FROM permissions WHERE permission = ?", (permission,))
        if not perm:
            raise PermissionNotFound("Permission introuvable.")
        permission_id = perm[0][0]

        # Attribuer la permission
        try:
            execute_query(
                "INSERT INTO user_permissions (user_id, permission_id) VALUES (?, ?)",
                (user_id, permission_id)
            )
        except sqlite3.IntegrityError:
            raise UserPermissionError("Permission déjà attribuée à cet utilisateur.")

    @staticmethod
    def check_permission(username, permission):
        result = fetch_query("""
            SELECT 1
            FROM users u
            JOIN user_permissions up ON u.id = up.user_id
            JOIN permissions p ON p.id = up.permission_id
            WHERE u.username = ? AND p.permission = ?
        """, (username, permission))
        if not result:
            raise UserPermissionError("Permission refusée.")
        return True