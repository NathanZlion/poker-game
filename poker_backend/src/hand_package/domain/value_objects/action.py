from dataclasses import dataclass
# from enum import Enum
from src.hand_package.presentation.schema.action import ActionType

# @dataclass(frozen=True)
# class ActionType(str, Enum):
#     FOLD = "FOLD"
#     CHECK = "CHECK" 
#     CALL = "CALL"
#     BET = "BET"
#     RAISE = "RAISE"
#     ALLIN = "ALL_IN"

@dataclass(frozen=True)
class ActionObject:
    success: bool = False
    message: str = ""
    next_actor: int | None = None
    current_actor: int | None = None
    maximum_bet: int = 0
    game_has_ended: bool = False
    pot_amount: int = 0


@dataclass(frozen=True)
class Action:
    amount: int
    description: str
    type: ActionType
