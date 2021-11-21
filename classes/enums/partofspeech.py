"""Enum type to represent a part of speech."""
from enum import Enum


class PartOfSpeech(Enum):
    """Enum type to represent all handled parts of speech."""
    DEFINITE_ARTICLE = "definite_article"
    INDEFINITE_ARTICLE = "indefinite_article"
    PERSONAL_PRONOUN = "personal_pronoun"
    POSSESSIVE_PRONOUN = "possessive_pronoun"
    OBJECT_PRONOUN = "object_pronoun"
    REFLEXIVE_PRONOUN = "reflexive)pronoun"
    ADJECTIVE = "adjective"
    NOUN = "noun"
    AMOUNT = "amount"
    VERB = "verb"
    ADVERB = "adverb"
    CONJUNCTION = "conjunction"
    PREPOSITION = "preposition"

    def can_follow_article_or_noun(self, part_of_speech: str) -> bool:
        """Checks if the current part of speech is an article or noun and the
        one given as an argument can follow it.

        Parameters
        ----------
        part_of_speech
            The following part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the current part of speech is an article and the
            one to follow is a part of speech that can come after it.
        """
        if self.value in (
                PartOfSpeech.DEFINITE_ARTICLE.value,
                PartOfSpeech.INDEFINITE_ARTICLE.value,
                PartOfSpeech.AMOUNT.value):
            if part_of_speech not in (
                    PartOfSpeech.NOUN.value, PartOfSpeech.ADJECTIVE.value):
                return False
        else:
            return False
        return True

    def can_follow_verb(self, part_of_speech: str) -> bool:
        """Checks if the current part of speech is a verb and the one given as
        an argument can follow it.

        Parameters
        ----------
        part_of_speech
            The following part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the current part of speech is a verb and the
            one to follow is a part of speech that can come after it.
        """
        if self.value == PartOfSpeech.VERB.value:
            if part_of_speech not in (
                    PartOfSpeech.DEFINITE_ARTICLE.value,
                    PartOfSpeech.ADVERB.value,
                    PartOfSpeech.NOUN.value,
                    PartOfSpeech.OBJECT_PRONOUN.value):
                return False
        else:
            return False
        return True

    def can_follow_personal_pronoun_or_noun(self, part_of_speech: str) -> bool:
        """Checks if the current argument is a personal pronoun or a noun and
        the one given as an argument can follow it.

        Parameters
        ----------
        part_of_speech
            The following part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the current part of speech is a personal pronoun or
            a noun and the one to follow isn't a verb.
        """
        if self.value in (
                PartOfSpeech.NOUN.value, PartOfSpeech.PERSONAL_PRONOUN.value):
            if part_of_speech != PartOfSpeech.VERB.value:
                return False
        else:
            return False
        return True
