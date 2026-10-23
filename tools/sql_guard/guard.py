"""Read-only SQL guard, multi-dialect.

First barrier: a single SELECT (or WITH ... SELECT, UNION/INTERSECT/MINUS), nothing
else. Second barrier is database-side (READ ONLY transaction / role) and is the
caller's responsibility.
"""

from __future__ import annotations

import re
from typing import Optional

import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError, TokenError

from .profiles import PROFILES

FORBIDDEN_NODES = tuple(
    getattr(exp, name)
    for name in (
        "Command", "Into", "Insert", "Update", "Delete", "Merge", "Create", "Drop",
        "Alter", "TruncateTable", "Transaction", "Commit", "Rollback", "Set",
        "Grant", "Declare", "Execute", "Lock",
    )
    if hasattr(exp, name)
)


class RejectedQuery(ValueError):
    pass


class SqlGuard:
    def __init__(self, dialect: str = "generic"):
        profile = PROFILES.get(dialect, PROFILES["generic"])
        self.dialect = dialect
        self.sqlglot_dialect = profile.get("sqlglot_dialect", dialect or None)
        self.forbidden_keywords = set(profile.get("forbidden_keywords", ()))
        self.allowed_functions = profile.get("allowed_functions")  # None => no check
        self.forbidden_objects = profile.get("forbidden_objects")

    def check(self, sql: str) -> None:
        if not sql or not sql.strip():
            raise RejectedQuery("empty query")

        # 1. parse: must be exactly one statement
        try:
            statements = sqlglot.parse(sql, read=self.sqlglot_dialect)
        except (ParseError, TokenError) as exc:
            raise RejectedQuery(f"parse error: {exc}") from exc
        statements = [s for s in statements if s is not None]
        if len(statements) != 1:
            raise RejectedQuery(f"expected exactly one statement, got {len(statements)}")

        stmt = statements[0]
        if not isinstance(stmt, (exp.Select, exp.Union, exp.Intersect, exp.Except, exp.With)):
            raise RejectedQuery(f"statement type not allowed: {type(stmt).__name__}")

        # 2. forbidden AST nodes anywhere
        for node in stmt.walk():
            if isinstance(node, FORBIDDEN_NODES):
                raise RejectedQuery(f"forbidden node: {type(node).__name__}")

        # 3. forbidden keywords outside literals/quoted identifiers
        self._check_keywords(sql)

        # 4. forbidden objects (packages) and unknown functions (dialect-specific)
        for node in stmt.walk():
            if isinstance(node, exp.Anonymous):
                name = node.name.upper() if hasattr(node, "name") else ""
                if self.forbidden_objects and self.forbidden_objects.match(name):
                    raise RejectedQuery(f"forbidden object/function: {name}")
                if self.allowed_functions is not None and name not in self.allowed_functions:
                    # could be a column; only treat as function if followed by (
                    raise RejectedQuery(f"function not in allow-list: {name}")

        # 5. INTO check (SELECT ... INTO)
        if re.search(r"\bINTO\b", sql, re.IGNORECASE):
            # allow only if inside a subquery? keep simple: reject any INTO
            raise RejectedQuery("INTO is not allowed")

    def _check_keywords(self, sql: str) -> None:
        # strip string literals and quoted identifiers before keyword scan
        scrubbed = re.sub(r"'[^']*'", "''", sql)
        scrubbed = re.sub(r'"[^"]*"', '""', scrubbed)
        tokens = re.findall(r"[A-Za-z_]+", scrubbed)
        for t in tokens:
            if t.upper() in self.forbidden_keywords:
                raise RejectedQuery(f"forbidden keyword: {t.upper()}")


def check(sql: str, dialect: str = "generic") -> None:
    SqlGuard(dialect).check(sql)
