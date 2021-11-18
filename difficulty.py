from enum import Enum

class Difficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    BEAST = 4

    @classmethod
    def get_description(self, difficulty):
        """
        Returns the description for a given input mode
        """
        if difficulty == 1:
            return "5 questions in 'popular' languages"
        elif difficulty == 2:
            return "5 questions in less 'popular' languages"
        elif difficulty == 3:
            return "10 questions in lesser known languages"
        elif difficulty == 4:
            return '26 questions in all available languages + 5 seconds to answer'