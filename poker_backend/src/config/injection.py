from functools import cache
from src.config.game import GameSettings
from src.config.database import DatabaseSettings


@cache
def get_game_settings():
    return GameSettings()


@cache
def get_db_settings():
    return DatabaseSettings()  # type: ignore
