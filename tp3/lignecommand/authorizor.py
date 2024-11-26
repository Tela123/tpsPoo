from exceptions import UserNotFound, NotLoggedIn, NotPermitted

class Authorizor:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}

    def add_permission(self, permission):
        if permission in self.permissions:
            raise ValueError(f"Permission '{permission}' already exists.")
        self.permissions[permission] = []

    def grant_permission(self, permission, username):
        if permission not in self.permissions:
            raise ValueError(f"Permission '{permission}' does not exist.")
        if username not in self.authenticator.users:
            raise UserNotFound(username)
        self.permissions[permission].append(username)

    def check_permission(self, permission, username):
        if permission not in self.permissions:
            raise ValueError(f"Permission '{permission}' does not exist.")
        if username not in self.permissions[permission]:
            raise NotPermitted(username, permission)
        if not self.authenticator.is_logged_in(username):
            raise NotLoggedIn(username)
        return True