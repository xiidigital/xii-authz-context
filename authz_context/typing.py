"""Type definitions for authorization context."""

from typing import NewType

# NewType definitions for strong typing
SubjectID = NewType("SubjectID", str)
OrgID = NewType("OrgID", str)
Permission = NewType("Permission", str)
