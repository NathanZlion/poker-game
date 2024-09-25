from fastapi import Depends
import psycopg2
from psycopg2.extensions import connection
from config.database import DatabaseSettings
from injection import get_db_settings
from typing import Generator


def getDatabaseConnection(
    settings: DatabaseSettings = Depends(get_db_settings),
) -> Generator[connection]:
    """
    Establishes a database connection using psycopg2 and yields it within a context manager.

    Args:
        settings: Database settings object.

    Returns:
        A generator that yields a psycopg2 connection.
    """

    db_connection_string = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    connection = psycopg2.connect(db_connection_string)

    try:
        yield connection
    except Exception as e:
        print(f"Could not connect to database {e}")
        raise
    finally:
        connection.close()
