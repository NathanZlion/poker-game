from dataclasses import dataclass
from config.injection import get_game_settings


@dataclass()
class CreateHand:
    playerCount: int = get_game_settings().PLAYER_COUNT
    stackSize: int = get_game_settings().STACK_SIZE
