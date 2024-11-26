from authenticator import Authenticator
from authorizor import Authorizor
from exceptions import AuthException

# Création d'instances
authenticator = Authenticator()
authorizor = Authorizor(authenticator)

# Exemple d'utilisation
if __name__ == "__main__":
    # Ajout d'utilisateurs
    try:
        authenticator.add_user("admin", "password123")
        authenticator.add_user("user1", "mypassword")
    except AuthException as e:
        print(e.message)

    # Connexion
    try:
        authenticator.login("admin", "password123")
        print("Admin connecté.")
    except AuthException as e:
        print(e.message)

    # Ajout et gestion des permissions
    try:
        authorizor.add_permission("view_reports")
        authorizor.grant_permission("view_reports", "admin")

        if authorizor.check_permission("view_reports", "admin"):
            print("Admin a la permission 'view_reports'.")
    except AuthException as e:
        print(e.message)

    # Déconnexion
    try:
        authenticator.logout("admin")
        print("Admin déconnecté.")
    except AuthException as e:
        print(e.message)