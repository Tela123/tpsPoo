class AuthException(Exception):
    def __init__(self, username, user=None):
        super().__init__(f"Authentication error for user: {username}")
        self.username = username
        self.user = user


class UsernameAlreadyExists(AuthException):
    def __init__(self, username):
        super().__init__(username)
        self.message = f"Username '{username}' already exists."


class UserNotFound(AuthException):
    def __init__(self, username):
        super().__init__(username)
        self.message = f"Username '{username}' not found."


class InvalidPassword(AuthException):
    def __init__(self, username):
        super().__init__(username)
        self.message = f"Invalid password for user '{username}'."


class NotLoggedIn(AuthException):
    def __init__(self, username):
        super().__init__(username)
        self.message = f"User '{username}' is not logged in."


class NotPermitted(AuthException):
    def __init__(self, username, permission):
        super().__init__(username)
        self.message = f"User '{username}' does not have permission '{permission}'."