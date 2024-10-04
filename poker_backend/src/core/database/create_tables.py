from src.core.database.database import getDatabaseConnection


def create_tables():
    create_extension_uuid = """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """

    create_hand_table = """
        CREATE TABLE IF NOT EXISTS hands (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            game_has_ended  BOOLEAN NOT NULL DEFAULT FALSE,
            hand_history TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """


    connection = getDatabaseConnection()
    with connection.cursor() as cursor:
        cursor.execute(create_extension_uuid)
        cursor.execute(create_hand_table)

    print("Tables creation compete")
    connection.commit()
