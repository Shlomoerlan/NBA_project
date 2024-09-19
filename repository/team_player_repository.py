import psycopg2
from psycopg2.extras import RealDictCursor
from toolz import curry, pipe


def get_db_connection():
    return psycopg2.connect("dbname=nba_db user=postgres password=1234 host=localhost",
                            cursor_factory=RealDictCursor)


def create_player_fantasy_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_fantasy (
            id SERIAL PRIMARY KEY,
            team_id INT REFERENCES team(id) ON DELETE CASCADE, 
            player_name VARCHAR(255) NOT NULL, 
            team VARCHAR(255) NOT NULL,  
            position VARCHAR(50) NOT NULL, 
            points INT NOT NULL, 
            games INT NOT NULL,  
            two_percent FLOAT NOT NULL, 
            three_percent FLOAT NOT NULL,
            atr FLOAT NOT NULL, 
            ppg_ratio FLOAT NOT NULL 
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("PlayerFantasy table created successfully!")


def create_player_fantasy(team_id, player):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO player_fantasy (team_id, player_name, team, position, points, games, two_percent, three_percent, atr, ppg_ratio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        team_id,
        player["player_name"],
        player["team"],
        player["position"],
        player["points"],
        player["games"],
        player["two_percent"],
        player["three_percent"],
        player["atr"],
        player["ppg_ratio"]
    ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Player {player['player_name']} added to team {team_id} in player_fantasy table.")


@curry
def find_player_by_name_and_season(player_name, season):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM players WHERE player_name = %s AND seasons = %s
    """, (player_name, season))

    player = cursor.fetchone()
    cursor.close()
    conn.close()

    return player


def get_player_by_name(player_name):
    seasons = [2024, 2023, 2022]
    player_search_fn = find_player_by_name_and_season(player_name)

    player = pipe(
        seasons,
        lambda seasons: map(player_search_fn, seasons),
        lambda results: next((p for p in results if p), None)
    )

    return player


def check_unique_names_and_positions(players):
    player_names = [player["player_name"] for player in players]
    positions = [player["position"] for player in players]

    if len(player_names) != len(set(player_names)):
        return {"error": "Duplicate player names found"}

    if len(positions) != len(set(positions)):
        return {"error": "Duplicate positions found"}

    return {"message": "Names and positions are unique"}


def insert_players_if_valid(players):
    conn = get_db_connection()
    cursor = conn.cursor()

    for player in players:
        if not player.get("player_id"):
            return {"error": f"Player {player.get('player_name', 'Unknown')} is missing player_id"}

        cursor.execute("""
            INSERT INTO players (player_id, player_name, team, position, points, games, two_percent, three_percent, atr, ppg_ratio, seasons)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            player["player_id"],
            player["player_name"],
            player["team"],
            player["position"],
            player["points"],
            player["games"],
            player["two_percent"],
            player["three_percent"],
            player["atr"],
            player["ppg_ratio"],
            player["seasons"]
        ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Players inserted successfully"}


@curry
def delete_team_references(cursor, team_id):
    cursor.execute("""
        DELETE FROM players WHERE team_id = %s
    """, (team_id,))


@curry
def delete_team_by_id(cursor, team_id):
    delete_team_references(cursor, team_id)

    cursor.execute("""
        DELETE FROM team WHERE id = %s
        RETURNING id
    """, (team_id,))

    deleted_team_id = cursor.fetchone()
    return deleted_team_id
