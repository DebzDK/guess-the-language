from enum import Enum


class InputMode(Enum):
    USER = 1
    FILE = 2
    AUTO = 3

    @classmethod
    def get_description(self, mode):
        """
        Returns the description for a given input mode
        """
        if mode == 2:
            return 'Load sentences from text file'
        if mode == 3:
            return 'Auto-generate sentences'
        return 'Enter sentence to translate (default)'
