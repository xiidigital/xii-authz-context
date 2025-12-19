"""xii-authz-context: Minimal, reusable authorization context.

This package provides a simple, framework-agnostic authorization context
that can be used as a foundation for authorization in any Python application.

It is NOT a complete IAM system - it does not handle authentication,
policy evaluation, or integration with specific frameworks.
"""

from .context import AnonymousAuthzContext, AuthzContext
from .exceptions import AuthenticationFailed, AuthorizationDenied, AuthzError
from .typing import OrgID, Permission, SubjectID

__version__ = "0.1.0"

__all__ = [
    "AuthzContext",
    "AnonymousAuthzContext",
    "AuthzError",
    "AuthenticationFailed",
    "AuthorizationDenied",
    "SubjectID",
    "OrgID",
    "Permission",
]
