from mariadb import connect
from mariadb.connections import Connection
import os


def _get_connection() -> Connection:
    return connect(
        user="kaloyan",
        password=os.environ.get("mariadb_root_pwd"),
        host="localhost",
        port=3306,
        database="Car Expenses",
    )


def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid

def multiple_insert_queries(queries: list):
    with _get_connection() as conn:
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()

        return cursor.lastrowid

def update_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount
