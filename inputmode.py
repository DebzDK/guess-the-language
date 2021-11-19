from enum import Enum


class InputMode(Enum):
    """
    Enum type to represent the game's different input modes.

    ...

    Members
    ----------
    USER : int
        integer representation of user input mode
    FILE : int
        integer representation of file input mode
    AUTO : int
        integer representation of auto input mode

    Methods
    -------
    get_description(cls, mode):
        Gets a description for a given input mode
    """
    USER = 1
    FILE = 2
    AUTO = 3

    @classmethod
    def get_description(cls, mode):
        """
        Returns the description for a given input mode
        """
        if mode == 2:
            return 'Load sentences from text file'
        if mode == 3:
            return 'Auto-generate sentences'
        return 'Enter sentence to translate (default)'
