import sqlparse
from sqlparse.sql import TokenList
from sqlparse.tokens import DML, DDL

DANGEROUS_KEYWORDS = {'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE'}

def is_safe_query(sql_query: str) -> bool:
    """Check if query is strictly read-only."""
    # 1. Keyword blocklist check
    parsed = sqlparse.parse(sql_query)
    for statement in parsed:
        for token in statement.flatten():
            if token.ttype in (DDL, DML) and token.value.upper() in DANGEROUS_KEYWORDS:
                return False
                
    # 2. Enforce read-only at the connection level (done in execution step)
    return True