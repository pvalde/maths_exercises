import sqlite3
import json
from typing import Dict, List, Any
import datetime
from utils.program_paths import ProgramPaths
from db.tag_db import TagDB


class ProblemDB:
    @staticmethod
    def add_problem(content: Dict, deck: str, tags: List[str] | None = None):
        # TODO update to support the addition of tags
        #       before adding tags and probleid
        content_json = json.dumps(content)
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        # add new tags:
        if tags:
            for tag in tags:
                # add tag to db if it does not exists there yet.
                TagDB.add_tag(tag)

        # add the rest
        try:
            with sqlite3.connect(
                ProgramPaths.get_user_db_path()
            ) as connection:
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                cursor.execute(
                    """
                               INSERT INTO problems (problem_content, problem_deck, problem_creation_date)
                               VALUES(
                                   ?,
                                   (SELECT deck_id FROM decks WHERE deck_name = ?),
                                   ?
                                     );
                               """,
                    (
                        content_json,
                        deck,
                        date_str,
                    ),
                )

                if tags:
                    for tag in tags:
                        # add info th problems_tags table
                        cursor.execute(
                            """
                                    INSERT INTO problems_tags (problem_id, tag_id)
                                    VALUES (
                                        (SELECT problem_id FROM problems WHERE problem_content = ? ),
                                        (SELECT tag_id FROM tags WHERE tag_name = ?)
                                    );
                            """,
                            (content_json, tag),
                        )

                connection.commit()

        except sqlite3.OperationalError as e:
            raise Exception("Failed to open database:", e)
        except sqlite3.Error as e:
            raise Exception("Failed to open database:", e)

    @staticmethod
    def get_all_problems():
        """
        Returns a list containing tuplets with all the problems.
        """
        # TODO: implement it as an iterator
        try:
            with sqlite3.connect(
                ProgramPaths.get_user_db_path()
            ) as connection:
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                cursor.execute("SELECT * FROM problems;")
                problems: List[Any] = cursor.fetchall()
                return problems

        except sqlite3.OperationalError as e:
            raise Exception("Failed to open database:", e)
        except sqlite3.Error as e:
            raise Exception("Failed to open database:", e)
