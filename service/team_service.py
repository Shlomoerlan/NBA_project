from repository.player_repository import get_db_connection
from repository.team_repository import delete_team_by_id, get_players_by_position, get_team_by_id, \
    get_players_by_team_id


def get_players_by_position_service(position, season=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    fetch_players = get_players_by_position(cursor)
    players = fetch_players(position, season)

    cursor.close()
    conn.close()
    return players


def delete_team_service(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    delete_team = delete_team_by_id(cursor)
    team_id_deleted = delete_team(team_id)
    print(team_id_deleted)
    if not team_id_deleted:
        cursor.close()
        conn.close()
        return None

    conn.commit()
    cursor.close()
    conn.close()

    return team_id_deleted


def get_team_details_service(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    get_team = get_team_by_id(cursor)
    team = get_team(team_id)

    if not team:
        cursor.close()
        conn.close()
        return None

    get_players = get_players_by_team_id(cursor)
    players = get_players(team_id)

    cursor.close()
    conn.close()

    return {"team": team, "players": players}

