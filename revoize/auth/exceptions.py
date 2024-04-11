class RevoizeAuthError(Exception):
    pass


class NotAuthorizedException(RevoizeAuthError):
    pass
