from enum import Enum
from typing import List
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
    type : ActionType
    amount : int = 0
    description : str = "Action to perform."


class ActionResponse(BaseModel):
    """ActionResponse schema

    Attributes:
        id: str, the id of the hand
        success: bool, whether the action was successful or not
        message: str, the message of the action
        allowed_moves: List[ActionType], the allowed actions for the player who is going to make the next move
        logs: List[str], the logs of the actions that have been performed in the hand
        game_has_ended: bool, whether the game has ended or not
        pot_amount: int, the total pot amount in the hand

    """
    id: str = ""
    success: bool = False
    message: str = ""
    allowed_moves: List[ActionType] = []
    logs: List[str]
    game_has_ended: bool = False
    pot_amount: int
