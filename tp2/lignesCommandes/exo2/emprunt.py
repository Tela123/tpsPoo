from personne import Personne
from datetime import datetime, timedelta

# Classe Emprunt
class Emprunt:
    def __init__(self, livre, personne):
        self.livre = livre
        self.personne = personne
        self.date_emprunt = datetime.now()
        self.date_retour_prevue = self.date_emprunt + timedelta(days=14)
