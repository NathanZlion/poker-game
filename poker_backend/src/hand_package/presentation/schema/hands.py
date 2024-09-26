from dataclasses import field
from typing import List
from pydantic import BaseModel
from config.game import GameSettings
from config.injection import get_game_settings


class CreateHandModel(BaseModel):
    playerCount: int = field(
        default=get_game_settings().PLAYER_COUNT,
    )
    stackSize: int = field(
        default=get_game_settings().STACK_SIZE,
    )


class HandResponse(BaseModel):
    id: str = ""
    has_ended: bool = False
    number_of_players: int = 6
    small_blind_idx: int = 3
    big_blind_idx: int = 4
    dealer_idx: int = 2
    stack_size: int = 10000
    big_blind_size: int = 40
    players: List[str] = field(default_factory=list)
    state: str = field(default_factory=str)


class GetHandRequest(BaseModel):
    pass


class HandHistoryResponse(BaseModel):
    hands: List[HandResponse] = field(default_factory=list)
