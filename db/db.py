import sqlite3
from utils.program_paths import ProgramPaths


def check_or_create_user_db() -> None:
    """
    Connects to user database. If there is no database, creates one following
    a given schema.
    """
    try:
        with sqlite3.connect(ProgramPaths.get_user_db_path()) as conn:
            print(
                f"Opened SQLite3 database with version {sqlite3.sqlite_version} successfully."
            )
            cursor = conn.cursor()

        # TODO: move definition of program's schema to another file (a 'Constants' module)
        # TODO: resolve the structure of tags in the db (maybe using a middle table?)

        # enable foreign keys constraints
        cursor.execute("PRAGMA foreign_keys = ON;")

        # add tables
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS problems(
                    problem_id                 INTEGER PRIMARY KEY,
                    problem_topic              TEXT,
                    problem_review_count       INTEGER,
                    problem_last_review_date   TEXT,
                    problem_feedback           INTEGER,
                    problem_src                TEXT,
                    problem_deck               INTEGER,
                    problem_content            TEXT UNIQUE NOT NULL,
                    FOREIGN KEY (problem_deck) REFERENCES decks(deck_id) ON DELETE RESTRICT ON UPDATE CASCADE 
                    ); 
        """
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS decks(
                    deck_id                 INTEGER PRIMARY KEY,
                    deck_name               TEXT UNIQUE NOT NULL
                    ); 
        """
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS tags(
                        tag_id                 INTEGER PRIMARY KEY,
                        tag_name               TEXT UNIQUE NOT NULL
                        );
            """
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS problems_tags(
                    problem_id              INTEGER NOT NULL,
                    tag_id                  INTEGER NOT NULL,
                    FOREIGN KEY (problem_id) REFERENCES problems(problem_id),
                    FOREIGN KEY (tag_id)    REFERENCES tags(tag_id)
                    );
        """
        )

        conn.commit()

    except sqlite3.OperationalError as e:
        raise Exception("Failed to open database:", e)
