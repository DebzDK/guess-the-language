from enum import Enum


class Difficulty(Enum):
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
