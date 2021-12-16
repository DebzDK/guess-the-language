"""Enum type to represent a part of speech."""
from enum import Enum
from typing import List


class PartOfSpeech(Enum):
    """Enum type to represent all handled parts of speech.

    ...

    Methods
    -------
    is_a_noun(self) -> bool:
        Returns True if the part of speech represents a noun.
    is_a_personal_pronoun(self) -> bool:
        Returns True if the part of speech represents a personal pronoun.
    is_a_verb(self) -> bool:
        Returns True if the part of speech represents a verb.
    is_an_adjective(self) -> bool:
        Returns True if the part of speech represents an adjective.
    is_an_adverb(self) -> bool:
        Returns True if the part of speech represents an adverb.
    is_an_amount(self) -> bool:
        Returns True if the part of speech is an amount.
    is_an_article_or_amount(self) -> bool:
        Returns True if the part of speech is an article or amount.
    is_an_indefinite_article(self) -> bool:
        Returns True if the part of speech is an indefinite article.
    is_a_conjunction(self) -> bool:
        Returns True if the part of speech represents a conjuction.
    can_follow(part_of_speech: PartOfSpeech) -> bool:
        Returns True if one part of speech can follow another, otherwise False.
    can_work_in_structure(sentence_structure: List[PartOfSpeech],
            preceding_part_of_speech: PartOfSpeech) -> bool:
        Returns True if a part of speech makes sense in a given sentence
        structure and the preceding part of speech.
    """
    DEFINITE_ARTICLE = "definite_article"
    INDEFINITE_ARTICLE = "indefinite_article"
    PERSONAL_PRONOUN = "personal_pronoun"
    POSSESSIVE_PRONOUN = "possessive_pronoun"
    OBJECT_PRONOUN = "object_pronoun"
    REFLEXIVE_PRONOUN = "reflexive_pronoun"
    ADJECTIVE = "adjective"
    NOUN = "noun"
    AMOUNT = "amount"
    VERB = "verb"
    ADVERB = "adverb"
    CONJUNCTION = "conjunction"
    PREPOSITION = "preposition"

    def is_a_noun(self) -> bool:
        """Determines if the part of speech represents a noun.

        Returns
        -------
        bool
            Returns True if the part of speech represents a noun.
        """
        return self is PartOfSpeech.NOUN

    def is_a_personal_pronoun(self) -> bool:
        """Determines if the part of speech represents a personal pronoun.

        Returns
        -------
        bool
            Returns True if the part of speech represents a personal pronoun.
        """
        return self is PartOfSpeech.PERSONAL_PRONOUN

    def is_a_verb(self) -> bool:
        """Determines if the part of speech word is a verb.

        Returns
        -------
        bool
            Returns True if the part of speech represents a verb.
        """
        return self is PartOfSpeech.VERB

    def is_an_adjective(self) -> bool:
        """Determines if the part of speech word is an adjective.

        Returns
        -------
        bool
            Returns True if the part of speech represents an adjective.
        """
        return self is PartOfSpeech.ADJECTIVE

    def is_an_adverb(self) -> bool:
        """Determines if the part of speech represents an adverb.

        Returns
        -------
        bool
            Returns True if the part of speech represents an adverb.
        """
        return self is PartOfSpeech.ADVERB

    def is_an_amount(self) -> bool:
        """Determines if the part of speech represents an amount.

        Returns
        -------
        bool
            Returns True if the part of speech represents an amount.
        """
        return self is PartOfSpeech.AMOUNT

    def is_an_article_or_amount(self) -> bool:
        """Determines if the part of speech represents an article or amount.

        Returns
        -------
        bool
            Returns True if the part of speech represents an article or amount.
        """
        return self in (
            PartOfSpeech.DEFINITE_ARTICLE,
            PartOfSpeech.INDEFINITE_ARTICLE,
            PartOfSpeech.AMOUNT
        )

    def is_an_indefinte_article(self) -> bool:
        """Determines if the part of speech represents an indefinite article.

        Returns
        -------
        bool
            Returns True if the part of speech represents an indefinite
            article.
        """
        return self is PartOfSpeech.INDEFINITE_ARTICLE

    def is_a_conjunction(self) -> bool:
        """Determines if the part of speech represents a conjunction.

        Returns
        -------
        bool
            Returns True if the part of speech represents a conjunction.
        """
        return self is PartOfSpeech.CONJUNCTION

    def can_follow(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if one part of speech can follow another.

        Parameters
        ----------
        part_of_speech
            The preceding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the current part of speech can follow the
            preceding part, otherwise False.
        """
        if (self._can_follow_article_or_noun(part_of_speech) or
                self._can_follow_verb(part_of_speech) or
                self._can_follow_personal_pronoun_or_noun(part_of_speech) or
                self._can_follow_adverb(part_of_speech) or
                self._can_follow_adjective(part_of_speech)):
            return True
        return False

    def can_work_in_structure(
            self, sentence_structure: List["PartOfSpeech"],
            preceding_part_of_speech: "PartOfSpeech") -> bool:
        """Checks if one part of speech can follow another.

        Parameters
        ----------
        part_of_speech
            The preceding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the current part of speech can follow the
            preceding part, otherwise False.
        """
        if ((self.is_a_verb() and self in sentence_structure) or
                (self.is_an_adverb() and
                    preceding_part_of_speech.is_an_adjective()) or
                (self.is_an_adjective() and
                    preceding_part_of_speech.is_an_adverb())):
            return False
        return True

    def _can_follow_article_or_noun(
            self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceding part of speech is an article or noun and the
        current one can follow it.

        Parameters
        ----------
        part_of_speech
            The preceding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceding part of speech is an article or
            amount and the current part of speech can follow it.
        """
        if part_of_speech.is_an_article_or_amount():
            if self not in (PartOfSpeech.NOUN, PartOfSpeech.ADJECTIVE):
                return False
        else:
            return False
        return True

    def _can_follow_verb(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceding part of speech is a verb and the current
        part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceding part of speech is a verb and the
            current part of speech can follow it.
        """
        if part_of_speech is PartOfSpeech.VERB:
            if self not in (
                    PartOfSpeech.DEFINITE_ARTICLE,
                    PartOfSpeech.ADVERB,
                    PartOfSpeech.NOUN,
                    PartOfSpeech.OBJECT_PRONOUN):
                return False
        else:
            return False
        return True

    def _can_follow_personal_pronoun_or_noun(
            self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceding part of speech is a personal pronoun or
        a noun and the current part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceding part of speech is a personal pronoun
            or a noun and the current part of speech that
            isn't a verb.
        """
        if part_of_speech in (
                PartOfSpeech.NOUN, PartOfSpeech.PERSONAL_PRONOUN):
            if not self.is_a_verb():
                return False
        else:
            return False
        return True

    def _can_follow_adverb(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceding part of speech is an adverb and the current
        part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceding part of speech is an adverb and the
            current part of speech can follow it.
        """
        if part_of_speech.is_an_adverb():
            if self not in (
                    PartOfSpeech.ADJECTIVE,
                    PartOfSpeech.CONJUNCTION,
                    PartOfSpeech.PREPOSITION):
                return False
        else:
            return False
        return True

    def _can_follow_adjective(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceding part of speech is an adjective and the current one
        is a part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceding part of speech is an adjective and
            the current part of speech can follow it.
        """
        if part_of_speech is PartOfSpeech.ADJECTIVE:
            if not self.is_a_noun():
                return False
        else:
            return False
        return True

    def _can_follow_preposition(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceding part of speech is a preposition and the current one
        is a part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceding part of speech is a preposition and
            the current part of speech can follow it.
        """
        if part_of_speech is PartOfSpeech.PREPOSITION:
            if not self.is_a_noun():
                return False
        else:
            return False
        return True

    def _can_follow_object_pronoun(
            self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceding part of speech is an object pronoun and the
        current part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceding part of speech is an object pronoun
            and the current part of speech can come after it.
        """
        if part_of_speech is PartOfSpeech.OBJECT_PRONOUN:
            if self not in (
                    PartOfSpeech.CONJUNCTION,
                    PartOfSpeech.PREPOSITION):
                return False
        else:
            return False
        return True
