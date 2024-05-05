"""Exceptions file"""


class GameOverException(Exception):
    """Exception raised when game is over"""

    def __init__(self, *args: object) -> None:
        """Init method"""
        super().__init__(*args)
