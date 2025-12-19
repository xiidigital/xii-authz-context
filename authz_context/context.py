"""Authorization context implementation."""

from dataclasses import dataclass
from typing import Optional

from .exceptions import AuthorizationDenied
from .typing import OrgID, Permission, SubjectID


@dataclass(frozen=True)
class AuthzContext:
    """
    Frozen dataclass representing an authorization context.
    
    This class holds information about a subject's identity and permissions
    for authorization purposes. It does NOT handle authentication.
    
    Attributes:
        subject_id: Unique identifier for the subject
        username: Optional username of the subject
        email: Optional email of the subject
        org_id: Optional organization identifier
        org_unit: Optional organizational unit
        permissions: Frozen set of permissions granted to the subject
    """
    subject_id: SubjectID
    username: Optional[str] = None
    email: Optional[str] = None
    org_id: Optional[OrgID] = None
    org_unit: Optional[str] = None
    permissions: frozenset[Permission] = frozenset()
    
    def has_permission(self, permission: Permission) -> bool:
        """
        Check if the context has a specific permission.
        
        Args:
            permission: The permission to check for
            
        Returns:
            True if the permission is granted, False otherwise
        """
        return permission in self.permissions
    
    def require(self, permission: Permission) -> None:
        """
        Require a specific permission, raising an exception if not granted.
        
        Args:
            permission: The permission to require
            
        Raises:
            AuthorizationDenied: If the permission is not granted
        """
        if not self.has_permission(permission):
            raise AuthorizationDenied(
                f"Permission '{permission}' is required but not granted"
            )
    
    def require_context(self) -> None:
        """
        Require that the context is not anonymous.
        
        Raises:
            AuthorizationDenied: If the context is anonymous
        """
        if isinstance(self, AnonymousAuthzContext):
            raise AuthorizationDenied("Authentication required")


class AnonymousAuthzContext(AuthzContext):
    """
    Authorization context for anonymous (unauthenticated) subjects.
    
    This represents a context with no authenticated subject and no permissions.
    """
    
    def __init__(self) -> None:
        """Initialize an anonymous authorization context."""
        super().__init__(
            subject_id=SubjectID("anonymous"),
            username=None,
            email=None,
            org_id=None,
            org_unit=None,
            permissions=frozenset()
        )
