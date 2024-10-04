from functools import cache

from src.config.database import DatabaseSettings
from src.config.game import GameSettings


@cache
def get_game_settings():
    return GameSettings()


@cache
def get_db_settings():
    return DatabaseSettings()  # type: ignore
