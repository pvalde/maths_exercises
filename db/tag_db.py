import sqlite3
from utils.program_paths import ProgramPaths


class TagDB:
    @staticmethod
    def add_tag(tag: str):
        """
        Adds tag to the db. If tag already exists, does nothing.
        """
        tag_name = tag.strip()
        try:
            with sqlite3.connect(
                ProgramPaths.get_user_db_path()
            ) as connection:
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                cursor.execute(
                    "INSERT OR IGNORE INTO tags(tag_name) VALUES(?);",
                    (tag_name,),
                )

                connection.commit()

        except sqlite3.OperationalError as e:
            raise Exception("Failed to open database:", e)
        except sqlite3.Error as e:
            raise Exception("Failed to open database:", e)
