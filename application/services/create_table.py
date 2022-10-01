from application.services.db_connection import DBConnection


def create_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS phones (
                    phone_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    contact name TEXT NOT NULL,
                    phone value INTEGER NOT NULL
                )
            """
            )
