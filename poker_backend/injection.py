from config.database import DatabaseSettings
from config.game import GameSettings


def get_db_settings():
    return DatabaseSettings()


def get_game_settings():
    return GameSettings()
