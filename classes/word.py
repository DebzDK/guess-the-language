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

    Methods
    -------
    is_an_adjective() -> bool:
        Returns True if the word is an adjective.
    is_an_adverb() -> bool:
        Returns True if the word is an adverb.
    is_an_amount() -> bool:
        Returns True if the word is an amount.
    is_an_article_or_amount() -> bool:
        Returns True if the word is an article or amount.
    is_a_being_verb() -> bool:
        Returns True if the word is a being verb (i.e. 'is').
    is_a_name() -> bool:
        Returns True if the word is a name.
    is_a_noun() -> bool:
        Returns True if the word is a noun.
    is_a_person_noun() -> bool:
        Returns True if the word is a noun representing a person.
    is_a_personal_pronoun() -> bool:
        Returns True if the word is a personal pronoun.
    is_a_verb() -> bool:
        Returns True if the word is a verb.
    is_an_intransitive_verb() -> bool:
        Returns True if the word is an intransitive verb.
    is_an_irregular_verb() -> bool:
        Returns True if the word is an irregular verb.
    is_a_possessive_verb() -> bool:
        Returns True if the word is a possessive verb (i.e. 'have').
    is_a_place() -> bool:
        Returns True if the word is a noun representing a place.
    is_possessive() -> bool:
        Returns True if the word is a possessive type part of speech.
    is_in_third_person() -> bool:
        Returns True if the given word is a 3rd person pronoun.
    """

    # Constructor
    def __init__(
            self, value: str, part_of_speech: PartOfSpeech,
            specificity: str = ""):
        """Initialises the object with the passed parameters.

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
        # so we strip them to be on the safe side
        self._value = value.replace(" ", "")
        self._part_of_speech = part_of_speech
        self._specificity = specificity

    def __str__(self):
        """Modifies object string representation using when printing."""
        return self._value

    def __repr__(self):
        """Modifies object string representation."""
        return (f"<Word value: {self._value} "
                f"part_of_speech: {self._part_of_speech.name} "
                f"specificity: {self._specificity}")

    # Use of decorator to access _value
    @property
    def value(self):
        """Getter method for value property"""
        return self._value

    # Use of decorator to access _part_of_speech
    @property
    def part_of_speech(self):
        """Getter method for part_of_speech property"""
        return self._part_of_speech

    # Use of decorator to access _specificity
    @property
    def specificity(self):
        """Getter method for specificity property"""
        return self._specificity

    def is_an_adjective(self) -> bool:
        """Checks if the given word is an adjective.

        Returns
        -------
        bool
            Returns True if the given word is an adjective.
        """
        return self._part_of_speech.is_an_adjective()

    def is_an_adverb(self) -> bool:
        """Checks if the given word is an adverb.

        Returns
        -------
        bool
            Returns True if the given word is an adverb.
        """
        return self._part_of_speech.is_an_adverb()

    def is_an_amount(self) -> bool:
        """Checks if the given word is an amount.

        Returns
        -------
        bool
            Returns True if the given word is an amount.
        """
        return self._part_of_speech.is_an_amount()

    def is_an_article_or_amount(self) -> bool:
        """Checks if the given word is an article or amount.

        Returns
        -------
        bool
            Returns True if the given word is an article or amount.
        """
        return self._part_of_speech.is_an_article_or_amount()

    def is_a_being_verb(self) -> bool:
        """Checks if the given word is a 'being' verb (i.e. 'is').

        Returns
        -------
        bool
            Returns True if the given word is a 'being' verb.
        """
        return self._specificity == "being"

    def is_a_name(self) -> bool:
        """Checks if the given word is a name.

        Returns
        -------
        bool
            Returns True if the given word is a name.
        """
        return self._specificity == "name"

    def is_a_noun(self) -> bool:
        """Checks if the given word is a noun.

        Returns
        -------
        bool
            Returns True if the given word is a noun.
        """
        return self._part_of_speech.is_a_noun()

    def is_a_person_noun(self) -> bool:
        """Checks if the given word is a noun representing a person.

        Returns
        -------
        bool
            Returns True if the given word is a noun.
        """
        return (self._part_of_speech.is_a_noun() and
                self._specificity in ("people", "name"))

    def is_a_personal_pronoun(self) -> bool:
        """Checks if the given word is a personal pronoun.

        Returns
        -------
        bool
            Returns True if the given word is a personal pronoun.
        """
        return (self._part_of_speech.is_a_personal_pronoun() or
                (self.is_a_person_noun() and self._specificity == 'personal'))

    def is_a_place(self) -> bool:
        """Checks if the given word is a place.

        Returns
        -------
        bool
            Returns True if the given word is a place.
        """
        return self._specificity == "place"

    def is_a_verb(self) -> bool:
        """Checks if the given word is a verb.

        Returns
        -------
        bool
            Returns True if the given word is a verb.
        """
        return self._part_of_speech.is_a_verb()

    def is_an_intransitive_verb(self) -> bool:
        """Checks if the given word is an intransitive verb.

        Returns
        -------
        bool
            Returns True if the given word is an intransitive verb.
        """
        return self.is_a_verb() and self._specificity == "intransitive"

    def is_an_irregular_verb(self) -> bool:
        """Checks if the given word is an irregular verb.

        Returns
        -------
        bool
            Returns True if the given word is an irregular verb.
        """
        return self.is_a_verb() and (
            self.is_a_being_verb() or self.is_a_possessive_verb())

    def is_a_possessive_verb(self) -> bool:
        """Checks if the given word is a possessive verb (i.e. 'have').

        Returns
        -------
        bool
            Returns True if the given word is a possessive verb.
        """
        return self._specificity == "possessive"

    def is_in_the_third_person(self) -> bool:
        """Checks if the given word is a 3rd person pronoun.

        Returns
        -------
        bool
            Returns True if the given word is a 3rd person pronoun.
        """
        return self._value in ("he", "she", "it")

    def is_possessive(self) -> bool:
        """Checks if the given word is a possessive part of speech.

        Returns
        -------
        bool
            Returns True if the given word is a possessive part of speech.
        """
        return self._specificity == "possessive"
