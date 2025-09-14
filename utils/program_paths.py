from pathlib import Path
import sys
import os


class ProgramPaths:
    @staticmethod
    def get_program_dir() -> str:
        """
        Returns the program data folder's path as a string object. It depends
        on the OS on top of which the program is running.
        """
        match sys.platform:
            case "win32":
                raise Exception(
                    "The program has not been implemented for Win32 yet!"
                )
            case "darwin":
                raise Exception(
                    "The program has not been implemented for macOS yet!"
                )
            case "linux":
                return os.path.join(Path.home(), ".local/share/maths_problems")
            case _:
                raise Exception(
                    "The program doesn't support the '"
                    + sys.platform
                    + "' platform."
                )

    @staticmethod
    def get_list_of_users() -> list[str]:
        """
        Returns a list containing all existing users in current system.
        It checks directories under ../maths_problems/, each one corresponding to
        user.
        """
        users: list[str] = os.listdir(ProgramPaths.get_program_dir())

        users_final: list[str] = []

        for item in users:
            if os.path.isdir(
                os.path.join(ProgramPaths.get_program_dir(), item)
            ):
                users_final.append(item)

        return users_final

    @staticmethod
    def get_username() -> str:
        """
        Returns a string containing the current user's name.
        """
        # TODO
        return "user0"

    @staticmethod
    def get_user_dir() -> str:
        """
        Returns the current directory of user's data.
        If there is no directory, it will be created.
        It creates the user's media directory if it doesn't exists.
        """
        user_path: str = os.path.join(
            ProgramPaths.get_program_dir(), ProgramPaths.get_username()
        )
        user_media_path: str = user_path + "/media/"
        # print("user_dir_path ", user_path)
        # print("user_media_path: ", user_media_path)

        if not os.path.exists(user_path):
            os.makedirs(user_path)

        if not os.path.exists(os.path.join(user_media_path)):
            # print(user_media_path, "doesn't exists!")
            os.makedirs(user_media_path)

        return os.path.join(user_path)

    @staticmethod
    def user_db_exists(path: str) -> bool:
        """
        Returns True if there is a database for the current user, otherwise False.
        """
        return os.path.exists(
            os.path.join(
                ProgramPaths.get_user_dir(),
                ProgramPaths.get_username() + ".db",
            )
        )

    @staticmethod
    def get_user_db_path() -> str:
        """
        Returns the path for the current user's database.
        """
        return os.path.join(
            ProgramPaths.get_user_dir(), ProgramPaths.get_username() + ".db"
        )

    @staticmethod
    def get_user_media_dir() -> str:
        """
        Returns the path for the current user's media directory with a
        trailing '/'.
        """
        return ProgramPaths.get_user_dir() + "/media/"
