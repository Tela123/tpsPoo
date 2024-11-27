import hashlib

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.is_logged_in = False

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()