from datetime import datetime

class Note:
    note_id = 0
    """_summary_
    Le constructeur de la classe Note

    Attributes:
    - memo: str
    - balises: list
    - date_creation: datetime
    = note_id: int
    """
    def __init__(self, memo, balises):
        self.memo = memo
        self.balises = balises
        self.date_creation = datetime.now()
        self.note_id = Note.note_id
        Note.note_id += 1

    def correspondance(self, terme):
        '''
        Ceci est une methode qui recherche la correspondance
        d'un terme dans memo ou balises
        '''
        return terme.lower() in self.memo.lower() or terme.lower() in self.balises.lower()
    
note = Note("Ceci est une note créee", "test")
print(note.correspondance("note"))