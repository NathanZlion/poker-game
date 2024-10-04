from functools import cache

import psycopg2
from psycopg2.extensions import connection

from src.config.database import DatabaseSettings
from src.config.injection import get_db_settings


@cache
def getDatabaseConnection() -> connection:
    """
    Establishes a database connection using psycopg2 and yields
    it within a context manager.

    Args:
        settings: Database settings object.

    Returns:
        A generator that yields a psycopg2 connection.
    """

    try:
        settings: DatabaseSettings = get_db_settings()
        db_connection_string = (
            f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
            f"@db:5432/{settings.POSTGRES_DB}"
        )

        connection = psycopg2.connect(db_connection_string)

        return connection
    except Exception as e:
        print(f"Could not connect to database {e}")
        raise
