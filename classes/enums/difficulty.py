"""Enum to represent difficulty levels"""
from enum import Enum


class Difficulty(Enum):
    """
    Enum type to represent the game's different difficulty levels.

    ...

    Members
    ----------
    EASY : int
        The integer representation of the easy difficulty level.
    NORMAL : int
        The integer representation of the normal difficulty level.
    HARD : int
        The integer representation of the hard difficulty level.
    BEAST : int
        The integer representation of the beast difficulty level.

    Methods
    -------
    get_description(cls, difficulty: int) -> str:
        Gets a description for a given difficulty level.
    """
    EASY = 0
    NORMAL = 1
    HARD = 2
    BEAST = 3

    @classmethod
    def get_description(cls, difficulty: int) -> str:
        """Returns the description for a given input mode.

        Returns
        -------
        str
            The description for the given difficulty level.
        """
        if difficulty == 1:
            return "5 questions in less 'popular' languages"
        if difficulty == 2:
            return "10 questions in lesser known languages"
        if difficulty == 3:
            return (
                "24 questions in all available languages"
                " + 5 seconds to answer"
            )
        return "5 questions in 'popular' languages"
