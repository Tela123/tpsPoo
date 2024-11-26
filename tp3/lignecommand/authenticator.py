from exceptions import UsernameAlreadyExists, UserNotFound, InvalidPassword
from user import User

class Authenticator:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise UsernameAlreadyExists(username)
        self.users[username] = User(username, password)

    def login(self, username, password):
        if username not in self.users:
            raise UserNotFound(username)
        user = self.users[username]
        if not user.check_password(password):
            raise InvalidPassword(username)
        user.is_logged_in = True

    def logout(self, username):
        if username not in self.users:
            raise UserNotFound(username)
        self.users[username].is_logged_in = False

    def is_logged_in(self, username):
        if username not in self.users:
            raise UserNotFound(username)
        return self.users[username].is_logged_in