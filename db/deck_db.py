import sqlite3
from utils.program_paths import ProgramPaths
from typing import List, Tuple


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
                cur = conn.cursor()

            cur.execute(
                "SELECT deck_name FROM decks WHERE deck_name = ?", (deck_name,)
            )

            if len(cur.fetchall()) == 0:
                return False
            else:
                return True

        except sqlite3.OperationalError as e:
            raise Exception("Failed to open database:", e)

    @staticmethod
    def add_deck(deck_name: str) -> None:
        """
        Adds the deck 'deck_name' to the DB.
        """
        # connect to user's database.
        try:
            with sqlite3.connect(ProgramPaths.get_user_db_path()) as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO decks (deck_name) VALUES (?)", (deck_name,)
                )
                conn.commit()
        except sqlite3.OperationalError as e:
            raise Exception("Failed to open database:", e)
        except sqlite3.Error as e:
            raise Exception(f"Error adding new deck to DB: {e}.")

    @staticmethod
    def get_decks_all() -> List[str]:
        # connect to user's database.
        try:
            with sqlite3.connect(ProgramPaths.get_user_db_path()) as conn:
                cur = conn.cursor()

                cur.execute("SELECT deck_name FROM decks")

                decks: List[Tuple[str]] = cur.fetchall()

                decks_list: List[str] = []

                for tuple in decks:
                    decks_list.append(tuple[0])

                return decks_list

        except sqlite3.OperationalError as e:
            raise Exception("Failed to open database:", e)

    @staticmethod
    def remove_deck(deck_name: str):
        # connect to user's database
        try:
            with sqlite3.connect(ProgramPaths.get_user_db_path()) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = on;")
                cursor.execute(
                    "DELETE FROM decks WHERE deck_name = ?", (deck_name,)
                )

        except sqlite3.IntegrityError as e:
            raise Exception(
                f"Error: the deck '{deck_name}' is not empty.\n{e}"
            )
        except sqlite3.Error as e:
            raise Exception("Database Error:", e)

    @staticmethod
    def get_deck_by_id(id: int):
        try:
            with sqlite3.connect(
                ProgramPaths.get_user_db_path()
            ) as connection:
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys = on;")
                cursor.execute(
                    "SELECT deck_name FROM decks WHERE deck_id = ?",
                    (id,),
                )

            return cursor.fetchone()[0]

        except sqlite3.Error as e:
            raise Exception("Database Error:", e)
