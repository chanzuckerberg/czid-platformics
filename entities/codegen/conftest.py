import os


def file_exists(filename: str) -> bool:
    if os.path.exists(filename):
        return True
    return False


def file_does_not_exist(filename: str) -> bool:
    if os.path.exists(filename):
        return False
    return True
