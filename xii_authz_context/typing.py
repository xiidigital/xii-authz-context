"""Semantic types for authorization context."""

from typing import NewType

SubjectID = NewType("SubjectID", str)
OrgID = NewType("OrgID", str)
Permission = NewType("Permission", str)
