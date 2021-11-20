"""Class used to represent a word"""
from typing import List


class Word():
    """Super class for coupling words with their parts of speech.

    Creates a new Word object.

    Attributes
    ----------
    _parts_of_speech: List[str]
        parts of speech that the word fall under
    _value : str
        the word
    """

    # Constructor
    def __init__(self, value: str, parts_of_speech: List[str]):
        """Initialise the object with the passed parameters

        Parameters
        ----------
        value
            The word
        parts_of_speech
            The list of parts of speech that the word falls under
        """
        # A single word cannot have spaces
        # so we strip them to be on the safeside
        self._value = value.replace(" ", "")
        self._parts_of_speech = parts_of_speech

    def __str__(self):
        """Modify object string representation using when printing"""
        return self._value

    def __repr__(self):
        """Modify object string representation"""
        return ('<Word value: "%s" parts_of_speech: %s>'
                % (self._value, self._parts_of_speech))

    # Use of decorator to access _value
    @property
    def value(self):
        """Getter method for value property"""
        return self._value
