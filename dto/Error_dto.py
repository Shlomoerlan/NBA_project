from dataclasses import dataclass
from models.PlayerModel import PlayerStats
from models.TeamModel import FantasyTeam, PlayerFantasy


@dataclass
class PlayerErrorDto:
    message: str = None
    body: PlayerStats = None
    error: str = None


@dataclass
class TeamErrorDto:
    message: str = None
    body: FantasyTeam = None
    error: str = None
