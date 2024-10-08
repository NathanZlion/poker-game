# from dataclasses import field
from typing import List

from pydantic import BaseModel

from src.config.injection import get_game_settings
from src.hand_package.presentation.schema.action import ActionType


class CreateHandModel(BaseModel):
    """CreateHandModel schema

    Attributes:
        player_count: int, the number of players in the game
        stack_size: int, the stack size for each player during the start\
        of the game

    Default values are taken from the game settings if field is not provided.
    """

    player_count: int = get_game_settings().PLAYER_COUNT
    stack_size: int = get_game_settings().STACK_SIZE


class HandResponse(BaseModel):
    """HandResponse schema

    Attributes:
        id: str, the id of the hand
        allowed_actions: List[ActionType], the allowed actions for the player\
        who is going to make the next move
        logs: List[str], the logs of the actions that have been performed in\
        the hand
        game_has_ended: bool, whether the game has ended or not
    """

    id: str
    allowed_actions: List[ActionType]
    message: str
    logs: List[str]
    game_has_ended: bool
    pot_amount: int
    minimum_bet_or_raise_amount: int


class GetHandRequest(BaseModel):
    pass


class HandHistoryResponse(BaseModel):
    """HandHistoryResponse schema

    Attributes:
        id: str, the id of the hand
        stack: int, the stack of the player
        dealer: str, the dealer of the hand
        small_blind_player: str, the small blind player
        big_blind_player: str, the big blind player
        actions: str, the actions that have been performed in the hand
        hands: dict[str, str], the hands of the players
        winnings: dict[str, int], the winnings of the players
    """

    id: str
    stack: int
    dealer: str
    small_blind_player: str
    big_blind_player: str
    actions: str
    hands: dict[str, str]
    winnings: dict[str, int]
