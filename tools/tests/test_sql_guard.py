import pytest

from tools.sql_guard import RejectedQuery, check


@pytest.mark.parametrize("sql", [
    "SELECT 1",
    "SELECT a, b FROM t WHERE x = 1",
    "WITH cte AS (SELECT 1 AS n) SELECT n FROM cte",
    "SELECT 1 UNION SELECT 2",
])
def test_allowed_generic(sql):
    check(sql, dialect="generic")


@pytest.mark.parametrize("sql", [
    "INSERT INTO t VALUES (1)",
    "UPDATE t SET x = 1",
    "DELETE FROM t",
    "DROP TABLE t",
    "SELECT 1; DROP TABLE t",
    "",
])
def test_rejected_generic(sql):
    with pytest.raises(RejectedQuery):
        check(sql, dialect="generic")


def test_oracle_allows_builtin():
    check("SELECT SYS_CONTEXT('USERENV','SESSION_USER') FROM dual", dialect="oracle")


def test_oracle_rejects_unknown_function():
    with pytest.raises(RejectedQuery):
        check("SELECT my_pkg.do_thing(x) FROM t", dialect="oracle")


def test_multi_statement_rejected():
    with pytest.raises(RejectedQuery):
        check("SELECT 1; SELECT 2", dialect="postgres")
