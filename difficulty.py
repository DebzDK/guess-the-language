"""
Enum to represent difficulty levels
"""
from enum import Enum


class Difficulty(Enum):
    """
    Enum type to represent the game's different difficulty levels.

    ...

    Members
    ----------
    EASY : int
        integer representation of easy difficulty level
    NORMAL : int
        integer representation of normal difficulty level
    HARD : int
        integer representation of hard difficulty level
    BEAST : int
        integer representation of beast difficulty level

    Methods
    -------
    get_description(cls, mode):
        Gets a description for a given difficulty level
    """
    EASY = 0
    NORMAL = 1
    HARD = 2
    BEAST = 3

    @classmethod
    def get_description(cls, difficulty):
        """
        Returns the description for a given input mode
        """
        if difficulty == 1:
            return "5 questions in less 'popular' languages"
        if difficulty == 2:
            return "10 questions in lesser known languages"
        if difficulty == 3:
            return '26 questions in all available languages + 5 seconds to answer'
        return "5 questions in 'popular' languages"
