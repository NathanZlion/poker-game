from dataclasses import dataclass, field
from typing import List


@dataclass
class Hand:
    """
    Hand entity

    Attributes:
    - id: str
    - hand_history: str
    """
    id: str = ""
    hand_history: str = field(default_factory=str)

