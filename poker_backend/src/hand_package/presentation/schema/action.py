from enum import Enum
from typing import List, Sequence
from pydantic import BaseModel


class ActionType(str, Enum):
    """
    Enum for the type of action that can be performed in a poker game

    `FOLD` - Player folds their hand \n
    `CHECK` - Player checks \n
    `BET` - Player bets an amount \n
    `CALL` - Player calls the current bet \n
    `RAISE` - Player raises the current bet \n
    `ALL_IN` - Player goes all in \n
    """

    FOLD = "FOLD"
    CHECK = "CHECK"
    CALL = "CALL"
    BET = "BET"
    RAISE = "RAISE"
    ALLIN = "ALL_IN"


class ActionModel(BaseModel):
    hand_id : str
    amount : int
    description : str
    type : ActionType



class ActionResponse(BaseModel):
    success: bool = False
    message: str = ""
    allowed_moves: List[ActionType] = []
    game_has_ended: bool = False
    logs: List[str]
    pot_amount: int
