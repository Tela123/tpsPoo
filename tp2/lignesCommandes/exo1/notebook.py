from note import Note

class Notebook:
    '''
    Une liste de notes
    '''
    def __init__(self):
        self.notes = []

    def ajouter_note(self, memo, balises):
        self.notes.append(Note(memo, balises))

    def modifier_note(self, id, memo=None, balises=None):
        for note in self.notes:
            if note.note_id == id:
                if memo:
                    note.memo = memo
                if balises:
                    note.balises = balises
                break

    def rechercher_note(self,terme):
        '''
            cette methode permet de rechercher une note
        '''
        return [note for note in self.notes if note.correspondance(terme)]

    def rechercher_note_id(self, note_id):
        '''
            cette methode permet de rechercher une note par son identifiant unique.
        '''
        for note in self.notes:
            if note.note_id == note_id:
                return note
        return None