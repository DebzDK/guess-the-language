"""Enum to represent input mode"""
from enum import Enum


class InputMode(Enum):
    """
    Enum type to represent the game's different input modes.

    ...

    Members
    ----------
    USER : int
        The integer representation of the user input mode.
    FILE : int
        The integer representation of the file input mode.
    AUTO : int
        The integer representation of the auto-generated input mode.

    Methods
    -------
    get_description(cls, mode: int) -> str:
        Returns a description for a given input mode.
    """
    USER = 1
    FILE = 2
    AUTO = 3

    @classmethod
    def get_description(cls, mode: int) -> str:
        """Returns the description for a given input mode.

        Returns
        -------
        str
            The description of the given input mode.
        """
        if mode == 2:
            return 'Load sentences from text file'
        if mode == 3:
            return 'Auto-generate sentences'
        return 'Enter sentence to translate (default)'
