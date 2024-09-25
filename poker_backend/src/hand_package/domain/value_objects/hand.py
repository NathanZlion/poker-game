from dataclasses import dataclass

from config.game import GameSettings


@dataclass(frozen=True)
class CreateHand:
    playerCount: int = GameSettings.PLAYER_COUNT
    stackSize: int = GameSettings.STACK_SIZE
