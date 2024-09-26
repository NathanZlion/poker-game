from src.core.database.database import getDatabaseConnection


def create_tables():
    create_extension_uuid = """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """


    create_hand_table = """
        CREATE TABLE IF NOT EXISTS hands (
            id SERIAL PRIMARY KEY,
            hand_history TEXT NOT NULL
        );
    """


    print("Creating Tables.......")
    connection = getDatabaseConnection()
    with connection.cursor() as cursor:
        cursor.execute(create_extension_uuid)
        cursor.execute(create_hand_table)

    print("Tables created successfully.")
    connection.commit()
