from dataclasses import dataclass
from models.PlayerModel import PlayerStats


@dataclass
class PlayerErrorDto:
    message: str = None
    body: PlayerStats = None
    error: str = None
