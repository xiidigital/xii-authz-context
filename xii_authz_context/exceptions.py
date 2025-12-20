"""Authorization exceptions."""


class AuthzError(Exception):
    """
    Base exception for authorization-related errors.

    All security/permission errors raised by the authz-context
    MUST inherit from this class.
    """
    pass


class AuthenticationFailed(AuthzError):
    """
    Raised when the subject cannot be authenticated.

    Examples:
    - Missing credentials
    - Invalid or expired token
    - Untrusted issuer
    """
    pass


class AuthorizationDenied(AuthzError):
    """
    Raised when an authenticated subject lacks permission
    to perform the requested action.
    """
    pass
