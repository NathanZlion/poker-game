from dataclasses import dataclass
from enum import Enum
from typing import Sequence
from src.hand_package.presentation.schema.action import DealtCards as DealtCardsModel


@dataclass(frozen=True)
class ActionType(str, Enum):
    FOLD  = "FOLD"
    CHECK = "CHECK"
    CALL = "CALL"
    BET = "BET"
    RAISE = "RAISE"
    ALLIN = "ALL_IN"


@dataclass()
class DealtCards(DealtCardsModel):
    street_name: str
    card_string: str


@dataclass(frozen=True)
class ActionObject:
    success: bool = False
    message: str = ""
    next_actor: int | None = None
    current_actor: int | None = None
    possible_moves: Sequence[ActionType] = []
    maximum_bet: int = 0
    game_has_ended: bool = False
    dealt_cards: Sequence[DealtCards] = []
    pot_amount: int = 0


@dataclass(frozen=True)
class Action:
    hand_id: str
    amount: int
    description: str
    type: ActionType
