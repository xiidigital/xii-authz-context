"""Exception classes for authorization context."""


class AuthzError(Exception):
    """Base exception for authorization errors."""
    pass


class AuthenticationFailed(AuthzError):
    """Exception raised when authentication fails."""
    pass


class AuthorizationDenied(AuthzError):
    """Exception raised when authorization is denied."""
    pass
