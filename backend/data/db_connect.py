from mariadb import connect
from mariadb.connections import Connection
from data.api_keys import DB_PASSWORD


def _get_connection() -> Connection:
    return connect(
        user="root",
        password=DB_PASSWORD,
        host="localhost",
        port=3306,
        database="Car Expenses",
    )


def read_query(sql: str, sql_params: tuple[str] | tuple = ()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params: tuple[str] | tuple = ()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def multiple_insert_queries(queries: list[str]):
    with _get_connection() as conn:
        cursor = conn.cursor()
        for query in queries:
            cursor.execute(query)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params: tuple[str] | tuple = ()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount
