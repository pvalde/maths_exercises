import sqlite3
import platformFuns


def check_or_create_user_db() -> None:
    """
    Connects to user database. If there is no database, creates one following
    a given squema.
    """
    try:
        with sqlite3.connect(platformFuns.get_user_db_path()) as conn:
            print(
                f"Opened SQLite database with version {sqlite3.sqlite_version} successfully."
            )
            cur = conn.cursor()
    except sqlite3.OperationalError as e:
        raise Exception("Failed to open database:", e)

    # TODO: move definiton of program's squema to another file (a 'Constans' module)
    cur.execute(
        """CREATE TABLE IF NOT EXISTS test(
                id INT PRIMARY KEY,
                a TEXT,
                b TEXT,
                c TEXT);
    """
    )

    conn.commit()
