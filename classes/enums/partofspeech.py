"""Enum type to represent a part of speech."""
from enum import Enum
from typing import List


class PartOfSpeech(Enum):
    """Enum type to represent all handled parts of speech.

    ...

    Methods
    -------
    can_follow(part_of_speech: PartOfSpeech) -> bool:
        Returns True if one part of speech can follow another, otherwise False.
    can_work_in_structure(sentence_structure: List[PartOfSpeech],
            preceeding_part_of_speech: PartOfSpeech) -> bool:
        Returns True if a part of speech makes sense in a given sentence
        structure and the preceeding part of speech.
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

    def can_follow(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if one part of speech can follow another.

        Parameters
        ----------
        part_of_speech
            The preceeding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the current part of speech can follow the
            preceeding part, otherwise False.
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
            preceeding_part_of_speech: "PartOfSpeech") -> bool:
        """Checks if one part of speech can follow another.

        Parameters
        ----------
        part_of_speech
            The preceeding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the current part of speech can follow the
            preceeding part, otherwise False.
        """
        if ((self is PartOfSpeech.VERB and self in sentence_structure) or
                (self is PartOfSpeech.ADVERB and
                    preceeding_part_of_speech is PartOfSpeech.ADJECTIVE)):
            return False
        return True

    def _can_follow_article_or_noun(
            self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceeding part of speech is an article or noun and the
        current one can follow it.

        Parameters
        ----------
        part_of_speech
            The preceeding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceeding part of speech is an article or
            amount and the current part of speech can follow it.
        """
        if part_of_speech in (
                PartOfSpeech.DEFINITE_ARTICLE,
                PartOfSpeech.INDEFINITE_ARTICLE,
                PartOfSpeech.AMOUNT):
            if self not in (PartOfSpeech.NOUN, PartOfSpeech.ADJECTIVE):
                return False
        else:
            return False
        return True

    def _can_follow_verb(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceeding part of speech is a verb and the current
        part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceeding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceeding part of speech is a verb and the
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
        """Checks if the preceeding part of speech is a personal pronoun or
        a noun and the current part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceeding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceeding part of speech is a personal pronoun
            or a noun and the current part of speech that
            isn't a verb.
        """
        if part_of_speech in (
                PartOfSpeech.NOUN, PartOfSpeech.PERSONAL_PRONOUN):
            if self is not PartOfSpeech.VERB:
                return False
        else:
            return False
        return True

    def _can_follow_adverb(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceeding part of speech is an adverb and the current
        part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceeding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceeding part of speech is an adverb and the
            current part of speech can follow it.
        """
        if part_of_speech is PartOfSpeech.ADVERB:
            if self not in (
                    PartOfSpeech.ADJECTIVE,
                    PartOfSpeech.CONJUNCTION):
                return False
        else:
            return False
        return True

    def _can_follow_adjective(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceeding part of speech is an adjective and the current one
        is a part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceeding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceeding part of speech is an adjective and
            the current part of speech can follow it.
        """
        if part_of_speech is PartOfSpeech.ADJECTIVE:
            if self is not PartOfSpeech.NOUN:
                return False
        else:
            return False
        return True

    def _can_follow_preposition(self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceeding part of speech is a preposition and the current one
        is a part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceeding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceeding part of speech is a preposition and
            the current part of speech can follow it.
        """
        if part_of_speech is PartOfSpeech.PREPOSITION:
            if self is not PartOfSpeech.NOUN:
                return False
        else:
            return False
        return True

    def _can_follow_object_pronoun(
            self, part_of_speech: "PartOfSpeech") -> bool:
        """Checks if the preceeding part of speech is an object pronoun and the
        current part of speech can follow it.

        Parameters
        ----------
        part_of_speech
            The preceeding part of speech to evaluate.

        Returns
        ----------
        bool
            Returns True if the preceeding part of speech is an object pronoun
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
