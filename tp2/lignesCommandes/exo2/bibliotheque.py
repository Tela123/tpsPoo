from emprunt import Emprunt
from livre import Livre
from personne import Personne

# Classe Bibliotheque
class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.personnes = []
        self.emprunts = []

    def ajouter_livre(self):
        titre = input("Entrez le titre du livre: ")
        auteur = input("Entrez l'auteur du livre: ")
        annee = input("Entrez l'année de publication: ")
        livre = Livre(titre, auteur, annee)
        self.livres.append(livre)
        print(f"Livre '{titre}' ajouté avec succès.")

    def ajouter_personne(self):
        nom = input("Entrez le nom de la personne: ")
        prenom = input("Entrez le prénom de la personne: ")
        nummembre = input("Entrez le numéro de membre: ")
        personne = Personne(nom, prenom, nummembre)
        self.personnes.append(personne)
        print(f"Personne '{nom} {prenom}' ajoutée avec succès.")

    def emprunter_livre(self):
        titre = input("Entrez le titre du livre à emprunter: ")
        nummembre = input("Entrez le numéro de membre de l'emprunteur: ")

        livre = next((livre for livre in self.livres if livre.titre == titre and livre.disponible), None)
        personne = next((personne for personne in self.personnes if personne.nummembre == nummembre), None)

        if not livre:
            print(f"Le livre '{titre}' n'est pas disponible ou n'existe pas.")
        elif not personne:
            print(f"Aucune personne trouvée avec le numéro de membre {nummembre}.")
        else:
            livre.disponible = False
            emprunt = Emprunt(livre, personne)
            self.emprunts.append(emprunt)
            print(f"Livre '{titre}' emprunté par {personne.nom} {personne.prenom}.")

    def retourner_livre(self):
        titre = input("Entrez le titre du livre à retourner: ")

        emprunt = next((emprunt for emprunt in self.emprunts if emprunt.livre.titre == titre), None)

        if emprunt:
            emprunt.livre.disponible = True
            self.emprunts.remove(emprunt)
            print(f"Livre '{titre}' retourné avec succès.")
        else:
            print(f"Aucun emprunt trouvé pour le livre '{titre}'.")

    def afficher_livres(self):
        if not self.livres:
            print("Aucun livre dans la bibliothèque.")
        else:
            print("Liste des livres :")
            for livre in self.livres:
                livre.afficher_details()

    def afficher_emprunts(self):
        if not self.emprunts:
            print("Aucun emprunt en cours.")
        else:
            print("Liste des emprunts :")
            for emprunt in self.emprunts:
                print(
                    f"Livre: {emprunt.livre.titre}, Emprunté par: {emprunt.personne.nom} {emprunt.personne.prenom}, "
                    f"Date de retour prévue: {emprunt.date_retour_prevue.strftime('%Y-%m-%d')}"
                )


# Fonction principale pour l'interaction
def menu():
    biblio = Bibliotheque()

    while True:
        print("\n--- MENU ---")
        print("1. Ajouter un livre")
        print("2. Ajouter une personne")
        print("3. Emprunter un livre")
        print("4. Retourner un livre")
        print("5. Afficher les livres")
        print("6. Afficher les emprunts")
        print("0. Quitter")

        choix = input("Entrez votre choix: ")

        if choix == "1":
            biblio.ajouter_livre()
        elif choix == "2":
            biblio.ajouter_personne()
        elif choix == "3":
            biblio.emprunter_livre()
        elif choix == "4":
            biblio.retourner_livre()
        elif choix == "5":
            biblio.afficher_livres()
        elif choix == "6":
            biblio.afficher_emprunts()
        elif choix == "0":
            print("Au revoir!")
            break
        else:
            print("Choix invalide, veuillez réessayer.")

