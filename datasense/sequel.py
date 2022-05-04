"""
SQL functions
"""

from typing import Dict

import psycopg2


def psycopg2_connection(params: Dict) -> psycopg2.connect:
    """
    Connect to the PostgreSQL database server.

    Parameters
    ----------
    database : str
        The name of the database.
    user : str
        The name of the user.
    password : str
        The password for the user.
    host : str
        The host address.
    port : int
        The port number.

    Example
    -------
    >>> connect_parameters = {
    >>>     "database": "mydb",
    >>>     "user": "postgres",
    >>>     "password": "password",
    >>>     "host": "localhost",
    >>>     "port": 5432
    >>> }
    >>> con = ds.psycopg2_connection(params=connect_parameters)
    """
    con = psycopg2.connect(**params)
    return con


__all__ = (
    "psycopg2_connection",
)
