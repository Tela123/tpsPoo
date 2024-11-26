from datetime import datetime, timedelta

# Classe Livre
class Livre:
    livre_id = 0
    def __init__(self, titre, auteur, annee):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.disponible = True
        self.livre_id=Livre.livre_id
        Livre.livre_id += 1

    def afficher_details(self):
        statut = "Disponible" if self.disponible else "Emprunté"
        print(f"Id: {self.livre_id} Livre: {self.titre}, Auteur: {self.auteur}, Année: {self.annee}, Statut: {statut}")
