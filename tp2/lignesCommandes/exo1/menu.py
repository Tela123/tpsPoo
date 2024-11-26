from notebook import Notebook

class Menu:
    def __init__(self):
        self.notebook = Notebook()
        
        self.choix = {
            "1": self.ajouter_note,
            "2": self.afficher_notes,
            "3": self.rechercher_note,
            "4": self.modifier_note,
            "5": self.quitter
        }

    def afficher_menu(self):
        print("""
        __MENU__
        1. Ajouter une note
        2. Afficher les notes
        3. Rechercher une note
        4. Modifier une note
        5. Quitter le programme
              """)
    
    def ajouter_note(self):
        '''
        Cette methode permet d'ajouter une note
        '''
        memo = input("Entrez le contenur de la note:")
        balises = input("Entrez les balises (séparées par des virgules): ")
        self.notebook.ajouter_note(memo, balises)
        print("La note a été ajoutée avec succès!")
        
        
    def afficher_notes(self):
        '''
        Cette methode permet d'afficher toutes note
        '''
        notes = self.notebook.notes
        if notes:
            for note in notes:
                print(f"ID: {note.note_id}, Mémo: {note.memo}, Balises: {note.balises}, Date: {note.date_creation}")
        else:
            print("Aucune note dans le carnet.")

    def rechercher_note(self):
        '''
            cette methode permet de rechercher une note
        '''
        terme=input("Entrez le terme de recherche : ")
        resultats = self.notebook.rechercher_note(terme)
        if resultats:
            for note in resultats:
                print(f"ID: {note.note_id}, Mémo: {note.memo}, Balises: {note.balises}, Date: {note.date_creation}")
        else:
            print("Aucune note ne correspond à votre recherche.")

    def modifier_note(self):
        '''
        Cette methode permet de modifier une note
        '''
        note_id = int(input("Entrez l'ID de la note à modifier : "))
        new_memo = input("Entrez le nouveau mémo (laisser vide pour ne pas modifier) : ")
        new_balise = input("Entrez les nouvelles balises (laisser vide pour ne pas modifier) : ")
        if self.notebook.modifier_note(note_id, new_memo or None, new_balise or None):
            print("Note modifiée.")
        else:
            print("Note introuvable.")

    def quitter(self):
        print("Merci d'avoir utilisé le programme")
        exit(0)

    def run(self):
        while True:
            self.afficher_menu()
            choix_option = input("Entre un choix:")
            action = self.choix.get(choix_option)
            if action:
                action()
            else:
                print("Choix invalide!")