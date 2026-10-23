"""Multi-dialect read-only SQL guard.

Usage:
    from tools.sql_guard import check
    check("SELECT 1", dialect="postgres")   # raises RejectedQuery on write
"""

from .guard import RejectedQuery, SqlGuard, check

__all__ = ["RejectedQuery", "SqlGuard", "check"]
