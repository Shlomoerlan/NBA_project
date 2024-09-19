import psycopg2
from psycopg2.extras import RealDictCursor


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



