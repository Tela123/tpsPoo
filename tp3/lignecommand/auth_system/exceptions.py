class AuthException(Exception):
    pass

class UserAlreadyExists(AuthException):
    pass

class UserNotFound(AuthException):
    pass

class PermissionAlreadyExists(AuthException):
    pass

class PermissionNotFound(AuthException):
    pass

class UserPermissionError(AuthException):
    pass