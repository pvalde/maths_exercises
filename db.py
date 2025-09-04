import sqlite3
import platformFuns


def check_or_create_user_db() -> None:
    """
    Connects to user database. If there is no database, creates one following
    a given schema.
    """
    try:
        with sqlite3.connect(platformFuns.get_user_db_path()) as conn:
            print(
                f"Opened SQLite3 database with version {sqlite3.sqlite_version} successfully."
            )
            cur = conn.cursor()
    except sqlite3.OperationalError as e:
        raise Exception("Failed to open database:", e)

    # TODO: move definition of program's schema to another file (a 'Constants' module)
    cur.execute(
        """CREATE TABLE IF NOT EXISTS exercises(
                exercise_id                 INTEGER PRIMARY KEY,
                exercise_topic              TEXT,
                exercise_review_count       INTEGER,
                exercise_last_review_date   TEXT,
                exercise_feedback           INTEGER,
                exercise_src                TEXT,
                exercise_TEXT,
                ); 
    """
    )

    conn.commit()
