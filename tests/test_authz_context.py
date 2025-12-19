"""Tests for authorization context."""

import pytest

from authz_context import (
    AnonymousAuthzContext,
    AuthenticationFailed,
    AuthorizationDenied,
    AuthzContext,
    AuthzError,
    OrgID,
    Permission,
    SubjectID,
)


class TestTypes:
    """Test type definitions."""
    
    def test_subject_id_creation(self):
        """Test SubjectID creation."""
        subject_id = SubjectID("user123")
        assert subject_id == "user123"
    
    def test_org_id_creation(self):
        """Test OrgID creation."""
        org_id = OrgID("org456")
        assert org_id == "org456"
    
    def test_permission_creation(self):
        """Test Permission creation."""
        permission = Permission("read:resource")
        assert permission == "read:resource"


class TestExceptions:
    """Test exception classes."""
    
    def test_authz_error_is_exception(self):
        """Test AuthzError is an Exception."""
        assert issubclass(AuthzError, Exception)
    
    def test_authentication_failed_is_authz_error(self):
        """Test AuthenticationFailed is an AuthzError."""
        assert issubclass(AuthenticationFailed, AuthzError)
    
    def test_authorization_denied_is_authz_error(self):
        """Test AuthorizationDenied is an AuthzError."""
        assert issubclass(AuthorizationDenied, AuthzError)
    
    def test_raise_authz_error(self):
        """Test raising AuthzError."""
        with pytest.raises(AuthzError):
            raise AuthzError("Test error")
    
    def test_raise_authentication_failed(self):
        """Test raising AuthenticationFailed."""
        with pytest.raises(AuthenticationFailed):
            raise AuthenticationFailed("Auth failed")
    
    def test_raise_authorization_denied(self):
        """Test raising AuthorizationDenied."""
        with pytest.raises(AuthorizationDenied):
            raise AuthorizationDenied("Access denied")


class TestAuthzContext:
    """Test AuthzContext class."""
    
    def test_create_minimal_context(self):
        """Test creating a minimal AuthzContext."""
        ctx = AuthzContext(subject_id=SubjectID("user123"))
        assert ctx.subject_id == "user123"
        assert ctx.username is None
        assert ctx.email is None
        assert ctx.org_id is None
        assert ctx.org_unit is None
        assert ctx.permissions == frozenset()
    
    def test_create_full_context(self):
        """Test creating a full AuthzContext."""
        permissions = frozenset([
            Permission("read:users"),
            Permission("write:users"),
        ])
        ctx = AuthzContext(
            subject_id=SubjectID("user123"),
            username="john_doe",
            email="john@example.com",
            org_id=OrgID("org456"),
            org_unit="engineering",
            permissions=permissions,
        )
        assert ctx.subject_id == "user123"
        assert ctx.username == "john_doe"
        assert ctx.email == "john@example.com"
        assert ctx.org_id == "org456"
        assert ctx.org_unit == "engineering"
        assert ctx.permissions == permissions
    
    def test_context_is_frozen(self):
        """Test that AuthzContext is frozen (immutable)."""
        ctx = AuthzContext(subject_id=SubjectID("user123"))
        with pytest.raises(Exception):  # FrozenInstanceError in dataclasses
            ctx.subject_id = SubjectID("user456")
    
    def test_has_permission_returns_true_when_granted(self):
        """Test has_permission returns True when permission is granted."""
        ctx = AuthzContext(
            subject_id=SubjectID("user123"),
            permissions=frozenset([Permission("read:users")]),
        )
        assert ctx.has_permission(Permission("read:users")) is True
    
    def test_has_permission_returns_false_when_not_granted(self):
        """Test has_permission returns False when permission is not granted."""
        ctx = AuthzContext(
            subject_id=SubjectID("user123"),
            permissions=frozenset([Permission("read:users")]),
        )
        assert ctx.has_permission(Permission("write:users")) is False
    
    def test_require_succeeds_when_permission_granted(self):
        """Test require succeeds when permission is granted."""
        ctx = AuthzContext(
            subject_id=SubjectID("user123"),
            permissions=frozenset([Permission("read:users")]),
        )
        # Should not raise
        ctx.require(Permission("read:users"))
    
    def test_require_raises_when_permission_not_granted(self):
        """Test require raises when permission is not granted."""
        ctx = AuthzContext(
            subject_id=SubjectID("user123"),
            permissions=frozenset([Permission("read:users")]),
        )
        with pytest.raises(AuthorizationDenied) as exc_info:
            ctx.require(Permission("write:users"))
        assert "write:users" in str(exc_info.value)
    
    def test_require_context_succeeds_for_regular_context(self):
        """Test require_context succeeds for regular context."""
        ctx = AuthzContext(subject_id=SubjectID("user123"))
        # Should not raise
        ctx.require_context()
    
    def test_require_context_raises_for_anonymous_context(self):
        """Test require_context raises for anonymous context."""
        ctx = AnonymousAuthzContext()
        with pytest.raises(AuthorizationDenied) as exc_info:
            ctx.require_context()
        assert "Authentication required" in str(exc_info.value)


class TestAnonymousAuthzContext:
    """Test AnonymousAuthzContext class."""
    
    def test_create_anonymous_context(self):
        """Test creating an AnonymousAuthzContext."""
        ctx = AnonymousAuthzContext()
        assert ctx.subject_id == "anonymous"
        assert ctx.username is None
        assert ctx.email is None
        assert ctx.org_id is None
        assert ctx.org_unit is None
        assert ctx.permissions == frozenset()
    
    def test_anonymous_is_authz_context(self):
        """Test that AnonymousAuthzContext is an AuthzContext."""
        ctx = AnonymousAuthzContext()
        assert isinstance(ctx, AuthzContext)
    
    def test_anonymous_has_no_permissions(self):
        """Test that anonymous context has no permissions."""
        ctx = AnonymousAuthzContext()
        assert ctx.has_permission(Permission("read:users")) is False
    
    def test_anonymous_require_raises(self):
        """Test that require raises for anonymous context."""
        ctx = AnonymousAuthzContext()
        with pytest.raises(AuthorizationDenied):
            ctx.require(Permission("read:users"))
    
    def test_anonymous_require_context_raises(self):
        """Test that require_context raises for anonymous context."""
        ctx = AnonymousAuthzContext()
        with pytest.raises(AuthorizationDenied):
            ctx.require_context()
