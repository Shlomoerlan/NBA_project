import requests
from typing import List
from toolz import curry
from models.PlayerModel import PlayerStats


@curry
def calculate_atr(player):
    turnovers = player['turnovers']
    assists = player['assists']
    atr = assists / turnovers if turnovers > 0 else 0
    player['atr'] = atr
    return player



@curry
def calculate_ppg_ratio(player):
    games = player['games']
    points = player['points']
    ppg_ratio = points / games if games > 0 else 0
    player['ppg_ratio'] = ppg_ratio
    return player


@curry
def create_player_stats(player):
    return PlayerStats(
        player_id=player["playerId"],
        player_name=player['playerName'],
        team=player['team'],
        position=player['position'],
        points=player['points'],
        games=player['games'],
        two_percent=player['twoPercent'],
        three_percent=player['threePercent'],
        atr=player['atr'],
        ppg_ratio=player['ppg_ratio'],
        seasons=player['season'],
    )


def fetch_player_data(api_url: str) -> List[PlayerStats]:
    response = requests.get(api_url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from API. Status code: {response.status_code}")
    player_data = response.json()
    return list(
        map(create_player_stats,
            map(calculate_ppg_ratio,
                map(calculate_atr,
                    player_data
                    )
                )
            )
    )




