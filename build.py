"""
Copyright 2021 Charles McMarrow
"""

# built-in
import os


# 3rd party
import PyInstaller.__main__


def build() -> None:
    """
    info: Builds backrooms into an executable.
    :return: None
    """
    PyInstaller.__main__.run([os.path.join(os.path.dirname(__file__), "main.py"),
                              "--onefile",
                              "--name", "backrooms"])


if __name__ == "__main__":
    build()
