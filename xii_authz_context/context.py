"""Authorization context data structures."""

from dataclasses import dataclass
from typing import FrozenSet, Optional

from .exceptions import AuthorizationDenied
from .typing import OrgID, Permission, SubjectID


@dataclass(frozen=True)
class AuthzContext:
    """Immutable authorization context for a subject.

    This class represents the authorization state of a subject (user, service, etc.)
    including their identity, organization membership, and permissions.
    """

    subject_id: SubjectID
    username: Optional[str] = None
    email: Optional[str] = None
    org_id: Optional[OrgID] = None
    org_unit: Optional[str] = None
    permissions: FrozenSet[Permission] = frozenset()

    def has_permission(self, permission: Permission) -> bool:
        """Check if the subject has a specific permission.

        Args:
            permission: The permission to check.

        Returns:
            True if the subject has the permission, False otherwise.
        """
        return permission in self.permissions

    def require(self, permission: Permission) -> None:
        """Require a specific permission, raising an exception if not present.

        Args:
            permission: The permission to require.

        Raises:
            AuthorizationDenied: If the subject does not have the permission.
        """
        if not self.has_permission(permission):
            raise AuthorizationDenied(
                f"Permission '{permission}' required but not granted"
            )

    def require_context(self) -> None:
        """Require that the subject has an organizational context.

        Raises:
            AuthorizationDenied: If org_id is None.
        """
        if self.org_id is None:
            raise AuthorizationDenied("Organizational context required but not present")


class AnonymousAuthzContext(AuthzContext):
    """Authorization context for anonymous users.

    This context represents an unauthenticated subject with no permissions.
    All optional fields are None and permissions is an empty frozenset.
    """

    def __init__(self) -> None:
        """Initialize anonymous authorization context."""
        super().__init__(
            subject_id=SubjectID("anonymous"),
            username=None,
            email=None,
            org_id=None,
            org_unit=None,
            permissions=frozenset(),
        )
