from dataclasses import dataclass, field


@dataclass
class Hand:
    """Hand entity

    Attributes:
        id: str, the id of the hand
        game_has_ended: bool, whether the game has ended or not
        hand_history: str, the history of the hand serialized as a string
    """

    game_has_ended: bool
    hand_history: str
    id: str = field(default="")
