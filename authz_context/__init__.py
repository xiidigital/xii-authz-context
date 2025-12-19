"""
xii-authz-context - Authorization context library.

This library provides authorization context management without authentication.
It is NOT an IAM system and has no dependencies.
"""

from .context import AnonymousAuthzContext, AuthzContext
from .exceptions import AuthenticationFailed, AuthorizationDenied, AuthzError
from .typing import OrgID, Permission, SubjectID

__version__ = "0.1.0"

__all__ = [
    # Main classes
    "AuthzContext",
    "AnonymousAuthzContext",
    # Exceptions
    "AuthzError",
    "AuthenticationFailed",
    "AuthorizationDenied",
    # Types
    "SubjectID",
    "OrgID",
    "Permission",
]
