"""
SQL functions
"""

from typing import Dict

import psycopg2


def psycopg2_connection(params: Dict) -> psycopg2.connect:
    """
    Connect to the PostgreSQL database server.
    """
    con = psycopg2.connect(**params)
    return con


__all__ = (
    "psycopg2_connection",
)
