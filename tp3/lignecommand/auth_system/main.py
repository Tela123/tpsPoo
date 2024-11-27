from database import init_db
from authenticator import Authenticator
from authorizor import Authorizor
from exceptions import AuthException

def main():
    init_db()  # Initialisation de la base de données

    while True:
        print("\n1. Ajouter un utilisateur")
        print("2. Ajouter une permission")
        print("3. Attribuer une permission")
        print("4. Vérifier une permission")
        print("5. Quitter")

        choice = input("Choix : ")
        try:
            if choice == "1":
                username = input("Nom d'utilisateur : ")
                password = input("Mot de passe : ")
                Authenticator.add_user(username, password)
                print("Utilisateur ajouté.")
            elif choice == "2":
                permission = input("Nom de la permission : ")
                Authorizor.add_permission(permission)
                print("Permission ajoutée.")
            elif choice == "3":
                username = input("Nom d'utilisateur : ")
                permission = input("Nom de la permission : ")
                Authorizor.assign_permission(username, permission)
                print("Permission attribuée.")
            elif choice == "4":
                username = input("Nom d'utilisateur : ")
                permission = input("Nom de la permission : ")
                if Authorizor.check_permission(username, permission):
                    print("L'utilisateur a la permission.")
            elif choice == "5":
                break
            else:
                print("Choix invalide.")
        except AuthException as e:
            print(f"Erreur : {e}")

if __name__ == "__main__":
    main()