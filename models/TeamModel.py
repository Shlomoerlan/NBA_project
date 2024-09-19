from dataclasses import dataclass
from typing import List


@dataclass
class PlayerFantasy:
    player_name: str
    team: str
    position: str
    points: int
    games: int
    two_percent: float
    three_percent: float
    atr: float
    ppg_ratio: float

    def __post_init__(self):
        if self.games == 0:
            raise ValueError("Games must be greater than 0 to calculate stats.")


@dataclass
class FantasyTeam:
    team_name: str
    players: List[PlayerFantasy]
