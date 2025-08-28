from pathlib import Path
import sys
import os

def get_program_dir() -> str:
    """
    Returns the program data folder's path as a string object. It depends on the
    os on top of which the program is running.
    """
    match sys.platform:
        case "win32":
            raise Exception("The program has not been implemented for Win32 yet!")
        case "darwin":
            raise Exception("The program has not been implemented for macOS yet!")
        case "linux":
            return os.path.join(
                Path.home(), ".local/share/maths_exercises"
            )
        case _:
            raise Exception(
                "The program doesn't support the '" + sys.platform + "' platform."
            )

def get_list_of_users() -> list[str]:
    """
    Returns a list containing all existing users in current system.
    It checks directories under ../maths_exercises/, each one corresponding to
    user.  
    """
    users: list[str] = os.listdir(get_program_dir())

    users_final: list[str] = []

    for item in users:
        if os.path.isdir(os.path.join(get_program_dir(), item)):
            users_final.append(item)

    return users_final


def get_username() -> str:
    """
    Returns a string containing the current user's name.
    """
    # TODO
    return "user1"


def get_user_dir() -> str:
    """
    Returns the current directory of user's data.
    If there is no directory, it will be created.
    """
    user_path: str = os.path.join(get_program_dir(), get_username())

    if not os.path.exists(user_path):
        os.makedirs(user_path)

    return os.path.join(user_path)


def user_db_exists(path: str) -> bool:
    """
    Returns True if there is a database for the current user, otherwise False.
    """
    return os.path.exists(os.path.join(get_user_dir(), get_username() + ".db"))


def get_user_db_path() -> str:
    """
    Returns the path for the current user's database.
    """
    return os.path.join(get_user_dir(), get_username() + ".db")
