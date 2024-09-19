from dataclasses import dataclass, field
from typing import List


@dataclass
class PlayerStats:
    player_id: str
    player_name: str
    team: str
    position: str
    seasons: int
    points: int
    games: int
    two_percent: float
    three_percent: float
    atr: float
    ppg_ratio: float
    id: int = None

    def __post_init__(self):
        if not self.seasons:
            raise ValueError("A player must have at least one season.")
