from livre import Livre
# Classe Personne
class Personne:
    def __init__(self, nom, prenom, nummembre):
        self.nom = nom
        self.prenom = prenom
        self.nummembre = nummembre

    def afficher_details(self):
        print(f"Nom: {self.nom}, Prénom: {self.prenom}, Numéro de membre: {self.nummembre}")

