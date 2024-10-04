from dataclasses import dataclass

from src.config.injection import get_game_settings


@dataclass()
class CreateHand:
    player_count: int = get_game_settings().PLAYER_COUNT
    stack_size: int = get_game_settings().STACK_SIZE
