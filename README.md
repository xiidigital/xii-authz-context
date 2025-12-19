# xii-authz-context

A lightweight Python authorization context library. **NOT** an IAM system - this library only handles authorization context, not authentication. Zero dependencies.

## Features

- **Simple authorization context management** - Track subject identity and permissions
- **Frozen dataclasses** - Immutable authorization contexts for thread safety
- **Type-safe** - Strong typing with NewType for IDs and permissions
- **Zero dependencies** - Pure Python 3.10+ with no external dependencies
- **Not IAM** - Does not handle authentication, only authorization context

## Installation

```bash
pip install xii-authz-context
```

## Quick Start

```python
from authz_context import (
    AuthzContext,
    AnonymousAuthzContext,
    SubjectID,
    OrgID,
    Permission,
    AuthorizationDenied,
)

# Create an authorization context
ctx = AuthzContext(
    subject_id=SubjectID("user123"),
    username="john_doe",
    email="john@example.com",
    org_id=OrgID("org456"),
    org_unit="engineering",
    permissions=frozenset([
        Permission("read:users"),
        Permission("write:users"),
    ])
)

# Check permissions
if ctx.has_permission(Permission("read:users")):
    print("User can read users")

# Require a permission (raises AuthorizationDenied if not granted)
try:
    ctx.require(Permission("delete:users"))
except AuthorizationDenied:
    print("Permission denied")

# Require authentication (raises AuthorizationDenied for anonymous contexts)
ctx.require_context()

# Create an anonymous context
anon_ctx = AnonymousAuthzContext()
print(anon_ctx.subject_id)  # "anonymous"
print(anon_ctx.permissions)  # frozenset()
```

## API Reference

### Types

- **SubjectID**: NewType for subject identifiers
- **OrgID**: NewType for organization identifiers  
- **Permission**: NewType for permission strings

### Exceptions

- **AuthzError**: Base exception for authorization errors
- **AuthenticationFailed**: Raised when authentication fails
- **AuthorizationDenied**: Raised when authorization is denied

### AuthzContext

Frozen dataclass representing an authorization context.

**Attributes:**
- `subject_id: SubjectID` - Unique identifier for the subject
- `username: Optional[str]` - Optional username
- `email: Optional[str]` - Optional email
- `org_id: Optional[OrgID]` - Optional organization ID
- `org_unit: Optional[str]` - Optional organizational unit
- `permissions: frozenset[Permission]` - Set of granted permissions

**Methods:**
- `has_permission(permission: Permission) -> bool` - Check if permission is granted
- `require(permission: Permission) -> None` - Require permission (raises AuthorizationDenied)
- `require_context() -> None` - Require non-anonymous context (raises AuthorizationDenied)

### AnonymousAuthzContext

Special authorization context for unauthenticated subjects. Inherits from AuthzContext with:
- `subject_id = "anonymous"`
- No permissions
- `require_context()` always raises AuthorizationDenied

## Design Philosophy

This library follows these principles:

1. **Authorization only** - No authentication logic
2. **No external dependencies** - Pure Python standard library
3. **Immutable contexts** - Thread-safe frozen dataclasses
4. **Explicit permissions** - Clear permission checking with strong typing
5. **Simple API** - Minimal surface area, easy to understand

## Requirements

- Python >= 3.10

## License

MIT License - see LICENSE file for details
