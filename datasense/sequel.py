"""
SQL functions
"""

import psycopg2


def psycopg2_connection(params: dict) -> psycopg2.connect:
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

    Returns
    -------
    con: psycopg2.connect
        A connection to the PostgreSQL database server.

    Example
    -------
    >>> import datasense as ds
    >>> connect_parameters = {
    ...     "database": "mydb",
    ...     "user": "postgres",
    ...     "password": "password",
    ...     "host": "localhost",
    ...     "port": 5432
    ... } # doctest: +SKIP
    >>> con = ds.psycopg2_connection(params=connect_parameters) # doctest: +SKIP
    """
    con = psycopg2.connect(**params)
    return con


__all__ = (
    "psycopg2_connection",
)
