import psycopg2
from psycopg2.extras import RealDictCursor
from toolz import curry


def get_db_connection():
    return psycopg2.connect("dbname=nba_db user=postgres password=1234 host=localhost",
                            cursor_factory=RealDictCursor)


def create_team_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team (
            id SERIAL PRIMARY KEY,  
            team_name VARCHAR(255) NOT NULL 
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Team table created successfully!")


def create_team(team_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO team (team_name)
        VALUES (%s)
    """, (team_name,))

    conn.commit()
    cursor.close()
    conn.close()


def get_team_id(team_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM team WHERE team_name = %s
    """, (team_name,))

    team_id = cursor.fetchone()['id']
    cursor.close()
    conn.close()

    if team_id is None:
        return None

    return team_id


@curry
def get_players_by_position(cursor, position, season=None):
    if season:
        cursor.execute("""
            SELECT * FROM players WHERE position = %s AND seasons = %s
        """, (position, season))
    else:
        cursor.execute("""
            SELECT * FROM players WHERE position = %s
        """, (position,))

    players = cursor.fetchall()
    return players


@curry
def delete_team_by_id(cursor, team_id):
    cursor.execute("""
        DELETE FROM team WHERE id = %s
        RETURNING id
    """, (team_id,))

    deleted_team_id = cursor.fetchone()
    return deleted_team_id


@curry
def get_team_by_id(cursor, team_id):
    cursor.execute("""
        SELECT id, team_name FROM team WHERE id = %s
    """, (team_id,))

    team = cursor.fetchone()
    return team


def get_team_by_id1(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, team_name
        FROM team
        WHERE id = %s
    """, (team_id,))
    team = cursor.fetchone()
    cursor.close()
    conn.close()
    if team:
        return {"team_id": team['id'], "team_name": team['team_name']}
    else:
        return None


@curry
def get_players_by_team_id(cursor, team_id):
    cursor.execute("""
        SELECT player_name, team, position, points, games, two_percent, three_percent, atr, ppg_ratio
        FROM player_fantasy
        WHERE team_id = %s
    """, (team_id,))

    players = cursor.fetchall()
    return players


def get_players_by_team_id1(team_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT player_name, team, position, points, games, two_percent, three_percent, atr, ppg_ratio
        FROM player_fantasy
        WHERE team_id = %s
    """, (team_id,))

    players = cursor.fetchall()
    cursor.close()
    conn.close()

    return [{"player_name": player['player_name'],
             "team": player['team'],
             "position": player['position'],
             "points": player['points'],
             "games": player['games'],
             "two_percent": player['two_percent'],
             "three_percent": player['three_percent'],
             "atr": player['atr'],
             "ppg_ratio": player['ppg_ratio']} for player in players]
