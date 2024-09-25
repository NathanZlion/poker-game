from core.database.database import getDatabaseConnection


def create_tables():
    create_extension_uuid = """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """

    create_game_state_table = """
        CREATE TABLE IF NOT EXISTS game_state (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            game_state JSONB
        )
    """

    create_game_history_table = """
        CREATE TABLE IF NOT EXISTS game_history (
            id SERIAL PRIMARY KEY,
            hand_id VARCHAR(255),
            stack INT,
            dealer VARCHAR(255),
            small_blind VARCHAR(255),
            big_blind VARCHAR(255),
            hands VARCHAR(255),
            actions VARCHAR(255),
            winnings VARCHAR(255)
        );
    """

    with getDatabaseConnection() as conn: # type: ignore
        with conn.cursor() as cursor:
            cursor.execute(create_extension_uuid)
            cursor.execute(create_game_state_table)
            cursor.execute(create_game_history_table)

        conn.commit()
