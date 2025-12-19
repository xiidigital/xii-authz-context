"""Authorization exceptions."""


class AuthzError(Exception):
    """Base exception for authorization errors."""

    pass


class AuthenticationFailed(AuthzError):
    """Raised when authentication fails."""

    pass


class AuthorizationDenied(AuthzError):
    """Raised when authorization is denied."""

    pass
