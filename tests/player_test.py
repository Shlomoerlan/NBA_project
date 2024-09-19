import pytest
from repository.player_repository import create_player, find_player_by_id, delete_player, get_all_players, \
 find_player_by_player_id, update_player, get_player_by_id_name
from models.PlayerModel import PlayerStats


@pytest.fixture(scope="function")
def setup_database():
    yield


def test_create_player(setup_database):
    player = PlayerStats(
        player_id="1",
        player_name="John Doe",
        team="Team A",
        position="Forward",
        points=500,
        games=25,
        two_percent=0.45,
        three_percent=0.35,
        atr=1.2,
        ppg_ratio=15.0,
        seasons=2021
    )
    created_id = create_player(player)
    assert created_id is not None



def test_get_all_players(setup_database):

    players = get_all_players()
    assert len(players) > 1


def test_find_player_by_id(setup_database):
    player = PlayerStats(
        player_id="1",
        player_name="John Doe",
        team="Team A",
        position="Forward",
        points=500,
        games=25,
        two_percent=0.45,
        three_percent=0.35,
        atr=1.2,
        ppg_ratio=15.0,
        seasons=2021
    )
    created_id = create_player(player)

    found_player = find_player_by_id(created_id)
    assert found_player is not None
    assert found_player.player_name == "John Doe"


def test_find_player_by_player_id(setup_database):

    found_player = find_player_by_player_id("henryaa01")
    assert found_player is not None
    assert found_player.player_name == 'Aarohbn Hekhnry'


def test_update_player(setup_database):
    player = PlayerStats(
        player_id="1",
        player_name="John Doe",
        team="Team A",
        position="Forward",
        points=500,
        games=25,
        two_percent=0.45,
        three_percent=0.35,
        atr=1.2,
        ppg_ratio=15.0,
        seasons=2021
    )
    created_id = create_player(player)

    updated_player = PlayerStats(
        player_id="1",
        player_name="John Updated",
        team="Team A",
        position="Forward",
        points=600,
        games=30,
        two_percent=0.50,
        three_percent=0.40,
        atr=1.5,
        ppg_ratio=18.0,
        seasons=2021
    )
    update_player(created_id, updated_player)

    found_player = find_player_by_id(created_id)
    assert found_player.player_name == "John Doe"
    assert found_player.points == 600


def test_delete_player(setup_database):
    player = PlayerStats(
        player_id="1",
        player_name="John Doe",
        team="Team A",
        position="Forward",
        points=500,
        games=25,
        two_percent=0.45,
        three_percent=0.35,
        atr=1.2,
        ppg_ratio=15.0,
        seasons=2021
    )
    created_id = create_player(player)

    delete_player(created_id)
    found_player = find_player_by_id(created_id)
    assert found_player is None


def test_get_player_by_name(setup_database):
    found_player = get_player_by_id_name("henryaa01")
    assert found_player is not None
    assert found_player['player_name'] == "Aarohbn Hekhnry"
