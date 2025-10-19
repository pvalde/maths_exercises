import sqlite3
import json
from typing import Dict, List
import datetime
from utils.program_paths import ProgramPaths
from db.tag_db import TagDB


class ProblemDB:
    @staticmethod
    def add_problem(content: Dict, deck: str, tags: List[str] | None = None):
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
        Generator function that returns a dictionary containing all the data of
        a single problem for each iteration.
        """
        try:
            with sqlite3.connect(
                ProgramPaths.get_user_db_path()
            ) as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                problems = cursor.execute("SELECT * FROM problems;")

                # iteration process:
                for problem in problems:
                    problem_dict = {}
                    for key in problem.keys():
                        problem_dict[key] = problem[key]

                    yield problem_dict

        except sqlite3.OperationalError as e:
            raise Exception("Failed to open database:", e)
        except sqlite3.Error as e:
            raise Exception("Failed to open database:", e)
