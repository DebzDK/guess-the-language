"""Class used to represent a word"""
from classes.enums.partofspeech import PartOfSpeech


class Word():
    """Class for coupling words with their parts of speech.

    Creates a new Word object.

    Attributes
    ----------
    _value : str
        The word.
    _part_of_speech: PartOfSpeech
        The part of speech that the word falls under.
    _specificity : str
        The type of part of speech that the word falls under.
    """

    # Constructor
    def __init__(
            self, value: str, part_of_speech: PartOfSpeech,
            specificity: str = ""):
        """Initialise the object with the passed parameters.

        Parameters
        ----------
        value
            The word.
        part_of_speech
            The part of speech that the word falls under.
        specificity
            The type of part of speech that the word falls under.
        """
        # A single word cannot have spaces
        # so we strip them to be on the safeside
        self._value = value.replace(" ", "")
        self._part_of_speech = part_of_speech
        self._specificity = specificity

    def __str__(self):
        """Modify object string representation using when printing."""
        return self._value

    def __repr__(self):
        """Modify object string representation."""
        return (f"<Word value: {self._value} "
                f"part_of_speech: {self._part_of_speech.name} "
                f"specificity: {self._specificity}")

    # Use of decorator to access _value
    @property
    def value(self):
        """Getter method for value property"""
        return self._value
