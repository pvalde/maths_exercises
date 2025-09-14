import sqlite3
from utils.program_paths import ProgramPaths


class DeckDB:
    @staticmethod
    def deck_exists(deck_name: str) -> bool:
        """
        If a deck with the name 'deck_name' exists, returns True. Otherwise,
        returns False.
        """

        # connect to user's database.
        try:
            with sqlite3.connect(ProgramPaths.get_user_db_path()) as conn:
                print(
                    f"Opened SQLite3 database with version {sqlite3.sqlite_version} successfully."
                )
                cur = conn.cursor()
        except sqlite3.OperationalError as e:
            raise Exception("Failed to open database:", e)

        cur.execute(
            "SELECT deck_name FROM decks WHERE deck_name = ?", (deck_name,)
        )

        if len(cur.fetchall()) == 0:
            return False
        else:
            return True


    @staticmethod
    def add_deck(deck_name: str) -> None:
        """
        Adds the deck 'deck_name' to the DB.
        """
        # connect to user's database.
        try:
            with sqlite3.connect(ProgramPaths.get_user_db_path()) as conn:
                print(
                    f"Opened SQLite3 database with version {sqlite3.sqlite_version} successfully."
                )
                cur = conn.cursor()
        except sqlite3.OperationalError as e:
            raise Exception("Failed to open database:", e)

        try:
            cur.execute(
                "INSERT INTO decks (deck_name) VALUES (?)", (deck_name,)
            )

        except sqlite3.Error as e:
            raise Exception(f"Error adding new deck to DB: {e}.")

        conn.commit()
