"""
Copyright 2021 Charles McMarrow
"""

# built-in
import os


def get_path(file_name: str) -> str:
    """
    info: Gets the absolute path to test file.
    :param file_name: str
    :return: str
    """
    return os.path.join(os.path.dirname(__file__), file_name)
