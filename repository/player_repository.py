from psycopg2.extras import RealDictCursor
from toolz import curry
import psycopg2
from config.sql_config import SQL_URL
from models.PlayerModel import PlayerStats


def get_db_connection():
    return psycopg2.connect(SQL_URL, cursor_factory=RealDictCursor)


def create_players_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            player_id VARCHAR(200) NOT NULL,
            player_name VARCHAR(200) NOT NULL,
            team VARCHAR(220) NOT NULL,
            position VARCHAR(220) NOT NULL,
            points INT NOT NULL,
            games INT NOT NULL,
            two_percent FLOAT NOT NULL,
            three_percent FLOAT NOT NULL,
            atr FLOAT NOT NULL,  
            ppg_ratio FLOAT NOT NULL,  
            seasons INT NOT NULL 
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()


def create_player(player):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO players (player_id, player_name, team, position, points, games, two_percent, three_percent, atr, ppg_ratio, seasons)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    """, (
        player.player_id,
        player.player_name,
        player.team,
        player.position,
        player.points,
        player.games,
        player.two_percent,
        player.three_percent,
        player.atr,
        player.ppg_ratio,
        player.seasons
    ))
    player_id = cursor.fetchone()['id']
    conn.commit()
    cursor.close()
    conn.close()
    return player_id


@curry
def insert_single_player(cursor, player):
    two_percent = player.two_percent if player.two_percent is not None else 0
    three_percent = player.three_percent if player.three_percent is not None else 0
    atr = player.atr if player.atr is not None else 0
    ppg_ratio = player.ppg_ratio if player.ppg_ratio is not None else 0

    cursor.execute("""
        INSERT INTO players (player_id, player_name, team, position, points, games, two_percent, three_percent, atr, ppg_ratio, seasons)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
        player.player_id,
        player.player_name,
        player.team,
        player.position,
        player.points,
        player.games,
        two_percent,
        three_percent,
        atr,
        ppg_ratio,
        player.seasons
    ))


def insert_players_to_db(players):
    conn = get_db_connection()
    cursor = conn.cursor()

    list(map(lambda player: insert_single_player(cursor, player), players))

    conn.commit()
    cursor.close()
    conn.close()
    print("Players inserted successfully!")


def get_all_players():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    cursor.close()
    conn.close()
    return [PlayerStats(**p) for p in players]


def find_player_by_id(player_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE id = %s", (player_id,))
    player_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if player_data:
        return PlayerStats(**player_data)
    return None


@curry
def get_player_by_name(player_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM players WHERE player_id = %s
    """, (player_name,))
    player = cursor.fetchone()
    cursor.close()
    conn.close()
    return player





def find_player_by_player_id(player_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE player_id = %s", (player_id,))
    player_data = cursor.fetchone()
    cursor.close()
    conn.close()
    if player_data:
        return PlayerStats(**player_data)
    return None

@curry
def update_player(p_id, updated_player):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE players
        SET team = %s, position = %s, points = %s, games = %s, two_percent = %s, three_percent = %s, atr = %s, ppg_ratio = %s, seasons = %s
        WHERE id = %s
        """, (
        updated_player.team,
        updated_player.position,
        updated_player.points,
        updated_player.games,
        updated_player.two_percent,
        updated_player.three_percent,
        updated_player.atr,
        updated_player.ppg_ratio,
        updated_player.seasons,
        p_id
    ))
    conn.commit()
    cursor.close()
    conn.close()


@curry
def delete_player(p_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE id = %s", (p_id,))
    conn.commit()
    cursor.close()
    conn.close()


def delete_all_players():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players")
    conn.commit()
    cursor.close()
    conn.close()
