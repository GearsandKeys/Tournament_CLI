import sqlite3


def cursor_and_conn_to_db():
    tournament_table = "pokemon_tournament.db"
    conn = sqlite3.connect(tournament_table)
    cursor = conn.cursor()
    return cursor, conn


def close_conn(conn):
    conn.commit()
    conn.close()


def create_tables():
    cursor, conn = cursor_and_conn_to_db()

    # Create the Players table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Tournaments (
            id INTEGER PRIMARY KEY,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Rounds (
            round_id INTEGER PRIMARY KEY,
            tournament_id INTEGER,
            player1_id INTEGER,
            player2_id INTEGER,
            winner_id INTEGER,
            loser_id INTEGER,
            round_number INTEGER,
            round_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tournament_id) REFERENCES Tournaments (id),
            FOREIGN KEY (player1_id) REFERENCES Players (id),
            FOREIGN KEY (player2_id) REFERENCES Players (id),
            FOREIGN KEY (winner_id) REFERENCES Players (id),
            FOREIGN KEY (loser_id) REFERENCES Players (id)
        )
    """
    )

    close_conn(conn)


def get_player_name(player_id):
    cursor, conn = cursor_and_conn_to_db()
    player = cursor.execute(
        "SELECT name FROM Players WHERE id = ?", (player_id,)
    ).fetchone()
    player_name = player[0] if player else None

    close_conn(conn)
    return player_name


def add_players(players: list):
    cursor, conn = cursor_and_conn_to_db()

    for name in players:
        # Check if the player already exists
        cursor.execute("SELECT id FROM Players WHERE name = ?", (name,))
        existing_player = cursor.fetchone()

        if not existing_player:
            cursor.execute("INSERT INTO Players (name) VALUES (?)", (name,))

    close_conn(conn)


def init_db():
    create_tables()

    players = ["Nathan", "Angelina", "Gma V", "Gwen", "Toby", "Louis"]
    add_players(players)


def get_player_stats(player_id):
    cursor, conn = cursor_and_conn_to_db()
    cursor.execute(
        """
        SELECT
            wins,
            losses,
            CASE
                WHEN wins = 0 AND losses = 0 THEN 0
                WHEN losses = 0 THEN 100
                ELSE CAST(wins AS FLOAT) / (wins + losses) * 100
            END AS win_loss_ratio
        FROM (
            SELECT
                IFNULL(COUNT(CASE WHEN winner_id = ? THEN 1 END), 0) AS wins,
                IFNULL(COUNT(CASE WHEN loser_id = ? THEN 1 END), 0) AS losses
            FROM Rounds
            WHERE (player1_id = ? OR player2_id = ?)
                AND (winner_id IS NOT NULL OR loser_id IS NOT NULL)
                AND tournament_id IS NOT NULL
        )
    """,
        (player_id, player_id, player_id, player_id),
    )

    wins, losses, win_loss_ratio = cursor.fetchone()
    close_conn(conn)
    return wins, losses, win_loss_ratio


def get_players():
    cursor, conn = cursor_and_conn_to_db()

    cursor.execute("SELECT id, name FROM Players")
    players = cursor.fetchall()

    close_conn(conn)
    return players


def print_all_tournaments():
    cursor, conn = cursor_and_conn_to_db()

    cursor.execute("SELECT * FROM Tournaments")
    tournaments = cursor.fetchall()

    print("List of all tournaments:")
    for tournament_info in tournaments:
        print(tournament_info)

    close_conn(conn)


def create_tournament_and_return_id():
    cursor, conn = cursor_and_conn_to_db()

    cursor.execute("INSERT INTO Tournaments DEFAULT VALUES")
    tournament_id = cursor.lastrowid

    close_conn(conn)

    return tournament_id


def get_tournament_rankings(tournament_id):
    cursor, conn = cursor_and_conn_to_db()
    cursor.execute(
        """
        SELECT
            p.name,
            IFNULL(COUNT(CASE WHEN r.winner_id = p.id THEN 1 END), 0) AS wins,
            IFNULL(COUNT(CASE WHEN r.loser_id = p.id THEN 1 END), 0) AS losses,
            CASE
                WHEN IFNULL(COUNT(CASE WHEN r.loser_id = p.id THEN 1 END), 0) = 0 THEN 0
                ELSE IFNULL(COUNT(CASE WHEN r.winner_id = p.id THEN 1 END), 0) / IFNULL(COUNT(CASE WHEN r.loser_id = p.id THEN 1 END), 0)
            END AS win_loss_ratio
        FROM Players p
        LEFT JOIN Rounds r ON p.id = r.winner_id OR p.id = r.loser_id
        WHERE r.tournament_id = ?
        GROUP BY p.id, p.name
        ORDER BY wins DESC, losses ASC
    """,
        (tournament_id,),
    )

    rankings = []
    for row in cursor.fetchall():
        player_name, wins, losses, win_loss_ratio = row
        rankings.append((player_name, wins, losses, win_loss_ratio))

    close_conn(conn)
    return rankings


def get_rounds_without_winner():
    cursor, conn = cursor_and_conn_to_db()

    cursor.execute(
        """
        SELECT round_id, round_number, player1_id, player2_id
        FROM Rounds
        WHERE winner_id IS NULL
    """
    )

    rounds = cursor.fetchall()

    close_conn(conn)
    return rounds


def create_round(tournament_id, round_number, player1_id, player2_id):
    cursor, conn = cursor_and_conn_to_db()
    cursor.execute(
        """
        INSERT INTO Rounds (tournament_id, round_number, player1_id, player2_id)
        VALUES (?, ?, ?, ?)
    """,
        (tournament_id, round_number, player1_id, player2_id),
    )

    close_conn(conn)


def update_winner(round_id, winner_id, loser_id):
    cursor, conn = cursor_and_conn_to_db()

    cursor.execute(
        "UPDATE Rounds SET winner_id = ?, loser_id = ? WHERE round_id = ?",
        (winner_id, loser_id, round_id),
    )

    close_conn(conn)


def print_all_rounds():
    cursor, conn = cursor_and_conn_to_db()

    cursor.execute("SELECT * FROM Rounds")
    rounds = cursor.fetchall()

    print("List of all rounds:")
    for round_info in rounds:
        print(round_info)

    close_conn(conn)


def debug():
    print("Rounds")
    print_all_rounds()
    print("Tournaments")
    print_all_tournaments()
