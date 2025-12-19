# xii-authz-context

Minimal, reusable authorization context for Python applications.

## What IS this?

`xii-authz-context` is a **lightweight, framework-agnostic library** that defines an authorization context data structure. It provides:

- A clean `AuthzContext` dataclass to represent a subject's identity and permissions
- Semantic types for better code clarity (`SubjectID`, `OrgID`, `Permission`)
- Basic authorization exceptions
- No external dependencies

This is a **building block** for authorization systems, not a complete IAM solution.

## What is this NOT?

This library does **NOT**:

- Authenticate users (no login, no password handling, no JWT parsing)
- Evaluate complex policies (no RBAC, no ABAC, no policy engine)
- Integrate with frameworks (no Django, no FastAPI, no Flask)
- Provide database models or persistence
- Connect to identity providers (no Keycloak, no Auth0, no LDAP)
- Handle HTTP requests or responses

## Installation

```bash
pip install xii-authz-context
```

## Usage

### Basic usage

```python
from xii_authz_context import AuthzContext, SubjectID, OrgID, Permission

# Create an authorization context
ctx = AuthzContext(
    subject_id=SubjectID("user-123"),
    username="john.doe",
    email="john@example.com",
    org_id=OrgID("org-456"),
    org_unit="engineering",
    permissions=frozenset([
        Permission("read:documents"),
        Permission("write:documents"),
    ])
)

# Check permissions
if ctx.has_permission(Permission("read:documents")):
    print("User can read documents")

# Require a permission (raises AuthorizationDenied if not present)
ctx.require(Permission("write:documents"))

# Require organizational context (raises AuthorizationDenied if org_id is None)
ctx.require_context()
```

### Anonymous context

```python
from xii_authz_context import AnonymousAuthzContext

# Anonymous users have no permissions
anon = AnonymousAuthzContext()
print(anon.subject_id)  # "anonymous"
print(anon.has_permission(Permission("read:documents")))  # False
```

### Error handling

```python
from xii_authz_context import AuthorizationDenied, AuthenticationFailed

try:
    ctx.require(Permission("admin:delete"))
except AuthorizationDenied as e:
    print(f"Access denied: {e}")
```

## Valid use cases

✅ **As a foundation for authorization in microservices**  
You receive user context from an API gateway and map it to `AuthzContext`.

✅ **As a contract between authentication and business logic**  
Your auth middleware creates `AuthzContext`, business logic consumes it.

✅ **For testing authorization logic**  
Create `AuthzContext` instances with specific permissions in your tests.

✅ **As a type-safe way to pass authorization data**  
Instead of passing dicts or ad-hoc objects, use `AuthzContext`.

## Invalid use cases

❌ **Do NOT use this for complete IAM**  
You need a full IAM system (Keycloak, AWS IAM, etc.).

❌ **Do NOT use this for authentication**  
This library has no login, password, or token handling.

❌ **Do NOT expect policy evaluation**  
This library only stores permissions, it doesn't evaluate complex policies.

❌ **Do NOT expect framework integration**  
You must write the glue code to integrate with Django, FastAPI, etc.

## Design principles

- **Immutable**: `AuthzContext` is frozen, preventing accidental modifications
- **Explicit**: No magic, no hidden behavior, no global state
- **Minimal**: Zero dependencies, simple API
- **Reusable**: Works with any framework or no framework at all
- **Type-safe**: Uses semantic types for clarity

## License

Mozilla Public License 2.0 (MPL-2.0)
