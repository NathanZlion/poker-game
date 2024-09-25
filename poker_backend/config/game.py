from pydantic_settings import BaseSettings


class GameSettings(BaseSettings):
    PLAYER_COUNT: int = 6
    BIG_BLIND_SIZE: int = 40
    STACK_SIZE: int = 10_000
