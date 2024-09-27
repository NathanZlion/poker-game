from functools import cache
import psycopg2
from psycopg2.extensions import connection
from config.database import DatabaseSettings
from config.injection import get_db_settings



@cache
def getDatabaseConnection() -> connection:
    """
    Establishes a database connection using psycopg2 and yields it within a context manager.

    Args:
        settings: Database settings object.

    Returns:
        A generator that yields a psycopg2 connection.
    """

    try:
        settings: DatabaseSettings = get_db_settings()
        try:
            default_connection_string = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/postgres"
            connection = psycopg2.connect(default_connection_string)
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {settings.DB_NAME};")

            connection.close()
        except Exception as e:
            # Database with name already created
            pass

        db_connection_string = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        connection = psycopg2.connect(db_connection_string)

        return connection
    except Exception as e:
        print(f"Could not connect to database {e}")
        raise
