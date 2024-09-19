import pytest
from repository.team_repository import (
    get_team_by_id,
    get_team_by_id1,
)
from service.team_service import delete_team_service


@pytest.fixture(scope="function")
def setup_database():
    yield


def test_get_team_by_id(setup_database):
    found_team = get_team_by_id(10)
    assert found_team is not None


def test_delete_team_by_id(setup_database):
    delete_team_service(11)
    found_team = get_team_by_id1(11)
    print(found_team)
    assert found_team is None
