import sqlite3
from utils.program_paths import ProgramPaths
from db.tag_db import TagDB
import json
from typing import Dict, List


class ProblemDB:
    @staticmethod
    def add_deck(content: Dict, deck: str, tags: List[str] | None = None):
        # TODO update to support the addition of tags
        #       before adding tags and probleid
        content_json = json.dumps(content)

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
                               INSERT INTO problems (problem_content, problem_deck)
                               VALUES(
                                   ?,
                                   (SELECT deck_id FROM decks WHERE deck_name = ?)
                                     );
                               """,
                    (
                        content_json,
                        deck,
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
