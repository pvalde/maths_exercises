import sqlite3
import json
from typing import Dict, Generator, List, Any
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
    def get_all_problems() -> Generator[dict[str, Any], None, None]:
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

    @staticmethod
    def get_problems_by_deck(deck_name: str) -> Generator[dict[str, Any], None, None]:
        """
        Generator function that returns a dictionary containing all the data of
        a single problem for each iteration, where the problem's deck is
        'deck_name'.
        """
        try:
            with sqlite3.connect(
                ProgramPaths.get_user_db_path()
            ) as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")

                problems = cursor.execute("""
                        SELECT * FROM problems
                        WHERE problem_deck = 
                            (SELECT deck_id FROM decks WHERE deck_name = ?)
                        """, (deck_name,))
                
                #iteration process:
                for problem in problems:
                    problem_dict = {}
                    for key in problem.keys():
                        problem_dict[key] = problem[key]
                    yield problem_dict
        except sqlite3.Error as e:
            raise Exception("Failed to open database:", e)
    

    # @staticmethod
    # def get_problems_by_tag(tag_name: str) -> Generator[dict[str, Any], None, None]:
    #     """
    #     Generator function that returns a dictionary
    #     """
    #     try:
    #         with sqlite3.connect(
    #             ProgramPaths.get_user_db_path()
    #         ) as connection:
    #             connection.row_factory = sqlite3.Row
    #             cursor = connection.cursor()
    #             cursor.execute("PRAGMA foreign_keys = ON;")
    #             
    #             cursor.execute("""
    #                     SELECT problem_id FROM problems_tags
    #                     WHERE tag_id = (SELECT tag_id FROM tags WHERE tag = ?)
    #                     """, (tag_name,))
    #             
    #             problem_id = cursor.fetchone()
    #             while problem_id is not None:
    #                 print(problem_id[0])
    #                 id = problem_id[0]
    #                 problem = cursor.execute(
    #                         "SELECT * FROM problems WHERE problem_id = ?",
    #                         (id,))

    #                 problem_dict = {}
    #                 for key in problem.keys():
    #                     problem_dict[key] = problem[key]
    #                 yield problem_dict

    #     except sqlite3.Error as e:
    #         raise Exception("Failed to open database:", e)

