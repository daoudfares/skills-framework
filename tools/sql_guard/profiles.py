"""Dialect profiles for the SQL guard."""

from __future__ import annotations

# Common read-only forbidden keywords.
COMMON_KEYWORDS = {
    "INSERT", "UPDATE", "DELETE", "MERGE", "UPSERT", "TRUNCATE",
    "CREATE", "ALTER", "DROP", "RENAME", "PURGE", "FLASHBACK",
    "GRANT", "REVOKE", "AUDIT", "NOAUDIT",
    "EXEC", "EXECUTE", "CALL", "BEGIN", "DECLARE",
    "COMMIT", "ROLLBACK", "SAVEPOINT", "LOCK", "SET", "INTO",
    "ANALYZE", "EXPLAIN", "SHUTDOWN", "STARTUP",
}

# Oracle native functions sqlglot does not recognise (Anonymous nodes allowed).
ORACLE_FUNCTIONS = {
    "SYS_CONTEXT", "SYS_EXTRACT_UTC", "SYS_GUID", "TRUNC", "NUMTODSINTERVAL", "NUMTOYMINTERVAL", "DUMP",
    "ORA_HASH", "WM_CONCAT", "LNNVL", "NANVL", "SOUNDEX", "TRANSLATE", "CHR", "ASCII", "INITCAP", "RTRIM",
    "LTRIM", "REPLACE", "BITAND", "SIGN", "CEIL", "FLOOR", "POWER", "SQRT", "ABS", "NEXT_DAY", "NEW_TIME",
    "FROM_TZ", "TZ_OFFSET", "TO_TIMESTAMP", "TO_TIMESTAMP_TZ", "TO_CLOB", "TO_NCHAR", "TO_CHAR", "TO_DATE",
    "TO_NUMBER", "RAWTOHEX", "HEXTORAW", "REGEXP_SUBSTR", "REGEXP_REPLACE", "REGEXP_INSTR", "REGEXP_COUNT",
    "REGEXP_LIKE", "LISTAGG", "XMLAGG", "XMLELEMENT", "EXTRACTVALUE", "RATIO_TO_REPORT", "NTILE",
    "CUME_DIST", "PERCENT_RANK", "MEDIAN", "STDDEV", "VARIANCE", "CORR", "USER", "UID", "VSIZE",
    "LENGTHB", "SUBSTRB", "INSTRB", "INSTR", "SUBSTR", "LPAD", "RPAD", "TO_YMINTERVAL", "TO_DSINTERVAL",
    "ROWIDTOCHAR", "FIRST_VALUE", "LAST_VALUE", "ADD_MONTHS", "MONTHS_BETWEEN", "LAST_DAY", "DECODE",
    "NVL", "NVL2", "GREATEST", "LEAST", "MOD", "ROUND", "LENGTH", "UPPER", "LOWER", "TRIM", "CONCAT",
    "STANDARD_HASH", "SESSIONTIMEZONE", "DBTIMEZONE", "SYSTIMESTAMP", "SYSDATE", "EXTRACT",
}

import re as _re

PROFILES = {
    "generic": {
        "sqlglot_dialect": None,
        "forbidden_keywords": COMMON_KEYWORDS,
        "allowed_functions": None,
        "forbidden_objects": None,
    },
    "postgres": {
        "sqlglot_dialect": "postgres",
        "forbidden_keywords": COMMON_KEYWORDS,
        "allowed_functions": None,
        "forbidden_objects": None,
    },
    "snowflake": {
        "sqlglot_dialect": "snowflake",
        "forbidden_keywords": COMMON_KEYWORDS,
        "allowed_functions": None,
        "forbidden_objects": None,
    },
    "oracle": {
        "sqlglot_dialect": "oracle",
        "forbidden_keywords": COMMON_KEYWORDS,
        "allowed_functions": ORACLE_FUNCTIONS,
        "forbidden_objects": _re.compile(r"^(DBMS_(?!METADATA$)\w*|UTL_\w*|HTP|HTF|OWA\w*|SYS\.DBMS_\w*)$", _re.IGNORECASE),
    },
}
