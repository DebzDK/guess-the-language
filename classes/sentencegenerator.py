"""Class for generating random sentences."""
import random
import re
from typing import Dict, List, Tuple
from classes.sentence import Sentence
from classes.word import Word
from classes.gamedictionary import GameDictionary
from classes.enums.language import Language
from classes.enums.partofspeech import PartOfSpeech


class SentenceGenerator():
    """A class used to help with sentence generation.

    This class will create the most basic sentence using the format:
        - Subject + Predicate
            where the subject can be a...
                - noun phrase
                    article (+ adjective) + noun
            and the predicate can be...
                - verb + (noun phrase or adverb or pronoun (+ adverb))

    ...

    Methods
    -------
    generate_sentence(character_limit: int) -> Sentence:
        Generates and returns a sentence.
    """

    @classmethod
    def generate_sentence(cls, character_limit: int) -> Sentence:
        """Generates a sentence that follows a basic structure and adheres to a
        character limit.

        Returns
        -------
        Sentence
            A basic sentence.
        """
        sentence_structure = cls._get_sentence_structure()
        words = []
        excluded_parts = {}
        for count, part_of_speech in enumerate(sentence_structure):
            has_suitable_word = False
            while not has_suitable_word:
                # (only set to 'associative' when a preposition has been
                # manually added on L101 and the previous word was an
                # intransive verb (i.e. isn't followed by a direct object))
                desired_type = (
                    "associative" if count > 1 and
                    words[count - 1].is_an_intransitive_verb() else "")

                # Find a word for the pre-selected part of speech in the
                # sentence structure, given the character limit for the game
                # level, desired type of part of speech to get, and a list of
                # parts of speech to exclude when searching.
                value, specificity = cls._select_word_for_part_of_speech(
                    part_of_speech, character_limit,
                    desired_type,
                    excluded_parts)

                # If not looking at the first part of speech in
                # sentence_structure,
                if count > 0:
                    preceding_word = words[len(words) - 1]
                    # conjugate the word if the part of speech is a verb.
                    if part_of_speech.is_a_verb():
                        value = cls._conjugate_verb_for_part_of_speech(
                            value, part_of_speech, preceding_word)
                    elif part_of_speech.is_a_noun():
                        # otherwise make it plural form if it's a noun that
                        # needs it.
                        value = cls._pluralise_noun(
                            value, part_of_speech, specificity, preceding_word)

                # If we're currently looking at the second part of speech
                # in sentence_structure,
                if count == 1:
                    preceding_word = sentence_structure[0]
                    if (preceding_word.is_an_indefinte_article() and
                            re.match("[a|e|i|o|u]", value)):
                        # add 'n' to the indefinite article (i.e. 'a') and
                        # replace the word
                        sentence_structure[0] = Word(
                            preceding_word.value + "n",
                            PartOfSpeech.INDEFINITE_ARTICLE, "indefinite"
                        )

                word = Word(
                    value.capitalize() if count == 0 else value,
                    part_of_speech, specificity
                )

                has_suitable_word, blacklist = (
                    cls._is_word_suitable_for_sentence(word, words)
                )

                if has_suitable_word:
                    words.append(word)
                    # Manual addition of preposition since prepositions
                    # haven't been included in valid sentence structure
                    # generation for the sake of simplicity (i.e. not handling
                    # every possible case where a preposition can fit in a
                    # sentence)
                    if word.is_an_intransitive_verb():
                        sentence_structure.insert(
                            count + 1, PartOfSpeech.PREPOSITION)
                else:
                    excluded_parts.update(blacklist)
                    if part_of_speech.is_an_adverb():
                        sentence_structure[count] = PartOfSpeech.NOUN

        return Sentence(words, Language.ENGLISH)

    @classmethod
    def _get_sentence_structure(cls) -> List[PartOfSpeech]:
        """Returns a random but valid order of parts of speech.

        Uses the random module to choose parts of speech, ensuring
        that the chosen part of speech can follow the previous.

        Returns
        ----------
        List[PartOfSpeech]
            A list of PartOfSpeech enums with a valid sentence order.
        """
        sentence_structure = cls._get_subject()
        found_predicate = False
        start_of_predicate_index = len(sentence_structure)

        list_of_choices = list(PartOfSpeech)
        temp_list_of_choices = list_of_choices.copy()

        while not found_predicate:
            preceding_part_of_speech = sentence_structure[-1]

            next_part = cls._get_next_part(
                preceding_part_of_speech, temp_list_of_choices)

            if next_part is None:
                break

            if next_part.can_follow(preceding_part_of_speech):
                if next_part.can_work_in_structure(
                        sentence_structure, preceding_part_of_speech):

                    sentence_structure.append(next_part)
                    temp_list_of_choices = list_of_choices.copy()

                    if not found_predicate:
                        found_predicate = cls._has_predicate(
                                sentence_structure, start_of_predicate_index)
                else:
                    temp_list_of_choices.remove(next_part)
                    list_of_choices.remove(next_part)
            else:
                temp_list_of_choices.remove(next_part)
        return sentence_structure

    @classmethod
    def _get_next_part(
            cls, preceding_part_of_speech: PartOfSpeech,
            temp_list_of_choices: List[PartOfSpeech]) -> PartOfSpeech:
        if preceding_part_of_speech.is_a_conjunction():
            next_part = cls._get_random_article()
        else:
            try:
                next_part = random.choice(temp_list_of_choices)
            except IndexError:
                return None
        return next_part

    @staticmethod
    def _select_word_for_part_of_speech(
            part_of_speech: PartOfSpeech, char_limit: int,
            desired_type: str = "",
            excluded_types: Dict[PartOfSpeech, str] = None) -> Word:
        """Selects a word for a given part of speech.

        Selects a word for a given part of speech at random until one is found
        that falls within a sentence's character limit for the current game's
        difficulty level.

        Parameters
        ----------
        part_of_speech
            The part of speech to find a word for.
        char_limit
            The character limit for the sentence.
        desired_type
            The desired type of part of speech to look for, if provided.
        excluded_types
            The types of parts_of_speech to ignore, if provided.

        Returns
        ----------
        Word
            A Word object if one is found that meets the criteria, otherwise
            None.
        """
        has_found_word = False
        found_word = ""

        while not has_found_word:
            found_word = GameDictionary.search_for_word_by_type(
                part_of_speech, desired_type, excluded_types)

            if char_limit - len(found_word) >= 0:
                has_found_word = True

        return found_word

    @classmethod
    def _get_subject(cls) -> List[PartOfSpeech]:
        """Gets a subject structure for a sentence.

        Following the format:
            definitve article (+ adjective) + noun

        Returns
        ----------
        List[PartOfSpeech]
            Returns a list of parts of speech that can make up the subject of a
            sentence.
        """
        structure = [cls._get_random_article()]
        next_part = random.choice([PartOfSpeech.ADJECTIVE, PartOfSpeech.NOUN])
        if next_part is PartOfSpeech.ADJECTIVE:
            structure.append(next_part)
            structure.append(PartOfSpeech.NOUN)
        else:
            structure.append(next_part)

        return structure

    @staticmethod
    def _has_subject(structure: List[PartOfSpeech]) -> bool:
        """Checks whether or not a given structure has enough parts to comprise
        the subject of a sentence.

        Determines if a structure starts with a subject, specifically:
            - noun phrase
                definitve article (+ adjective) + noun

        Parameters
        ----------
        structure
            A list of the parts of speech structuring a sentence.

        Returns
        ----------
        bool
            Returns True if structure has enough parts of speech to make a
            sentence.
        """
        if len(structure) > 1:
            if structure[0] in (
                    PartOfSpeech.DEFINITE_ARTICLE,
                    PartOfSpeech.INDEFINITE_ARTICLE):
                following_part = structure[1]

                if following_part is PartOfSpeech.NOUN:
                    return True
        return False

    @classmethod
    def _has_predicate(
            cls, structure: List[PartOfSpeech], predicate_index: int) -> bool:
        """Checks whether or not a given structure has enough parts to comprise
        the predicate of a sentence.

        Determines if a structure ends with a predicate, specifically:
            - verb + (noun phrase or or noun or adverb)

        Parameters
        ----------
        structure
            A list of the parts of speech structuring a sentence.
        predicate_index
            The index of the part of speech that marks the start of the
            predicate in the list.

        Returns
        ----------
        bool
            Returns True if structure has enough parts of speech to make a
            sentence.
        """
        if predicate_index > -1 and len(structure) > predicate_index + 1:
            start_of_predicate = structure[predicate_index]

            if start_of_predicate is PartOfSpeech.VERB:
                following_part = structure[predicate_index + 1]
                if ((following_part in (
                    PartOfSpeech.DEFINITE_ARTICLE,
                    PartOfSpeech.INDEFINITE_ARTICLE) and
                    cls._has_subject(structure[1:])) or
                        following_part in (
                            PartOfSpeech.OBJECT_PRONOUN, PartOfSpeech.NOUN,
                            PartOfSpeech.ADVERB)):
                    return True
        return False

    @staticmethod
    def _get_random_article() -> PartOfSpeech:
        """Gets a random article.

        Returns
        ----------
        PartOfSpeech
            Returns a definite or indefinite article.
        """
        return random.choice([
            PartOfSpeech.DEFINITE_ARTICLE,
            PartOfSpeech.INDEFINITE_ARTICLE
        ])

    @staticmethod
    def _is_word_suitable_for_sentence(
            word_to_add: Word, sentence: List[Word]) -> Tuple[bool, List[str]]:
        """Checks if a word is suitable for a given sentence.

        Attempts to determine if a word fits into a sentence given preceding
        words in the sentence.

        Parameters
        ----------
        word_to_add
            The word being evaluated.
        sentence
            The sentence the word is being added to.

        Returns
        ----------
        Tuple[bool, List[str]]
            Returns a tuple with value True and an empty list if the word is
            detemined to be 'suitable' for the sentence, otherwise a tuple
            with value False and a list of types to not include when
            searching for the next suitable word.
        """
        blacklist = {}

        reversed_sentence = sentence.copy()
        reversed_sentence.reverse()

        if len(sentence) > 0:
            for preceding_word in reversed_sentence:
                add_to_blacklist = False
                if preceding_word.is_an_article_or_amount():
                    if (word_to_add.is_possessive() or
                            word_to_add.is_a_place() or
                            word_to_add.is_a_name()):
                        add_to_blacklist = True

                if (preceding_word.is_an_irregular_verb() and
                        word_to_add.is_an_adverb()):
                    add_to_blacklist = True

                if ((preceding_word.is_an_adjective() or
                        preceding_word.is_a_noun()) and
                        word_to_add.is_a_noun() and
                        preceding_word.specificity !=
                        word_to_add.specificity):
                    add_to_blacklist = True

                if (word_to_add.is_a_verb() and preceding_word.is_a_noun() and
                        preceding_word.specificity == "food" and
                        not word_to_add.is_a_being_verb()):
                    add_to_blacklist = True

                if add_to_blacklist:
                    if word_to_add.part_of_speech not in blacklist:
                        blacklist[word_to_add.part_of_speech] = set()
                    blacklist[word_to_add.part_of_speech].add(
                        word_to_add.specificity)

        return (len(blacklist) == 0, blacklist)

    @staticmethod
    def _conjugate_verb_for_part_of_speech(
            word: str, part_of_speech_for_word: PartOfSpeech,
            preceding_word: Word) -> str:
        """Returns a conjugated verb.

        Based on basic English grammar rules, this method attempts to
        correctly conjugate a given verb based on the part of speech that it
        follows.

        Parameters
        ----------
        word
            The word to conjugate.
        part_of_speech_for_word
            The part of speech the given word falls under.
        preceding_word
            The word that comes before the word to conjugate.

        Returns
        -------
        str
            The conjugated verb.
        """
        if part_of_speech_for_word.is_a_verb():
            if word in ("am", "have"):
                if (preceding_word.is_in_the_third_person() or
                        preceding_word.is_a_noun()):
                    return "am" if word == "is" else "has"
                if preceding_word.is_in_the_second_person():
                    return "are" if word == "is" else "have"

            if (not preceding_word.is_an_irregular_verb() and
                    (preceding_word.is_a_name() or
                        preceding_word.is_a_noun() or
                        preceding_word.is_a_person_noun() or
                        (
                            preceding_word.is_a_personal_pronoun() and
                            preceding_word.value in ("he", "she", "it")
                        ))):
                return f"{word}{'e' if word[-1] == 'o' else ''}s"
        return word

    @staticmethod
    def _pluralise_noun(
            word: str, part_of_speech_for_word: PartOfSpeech,
            specificity: str, preceding_word: Word) -> str:
        """Returns the noun in plural form if needed.

        Based on basic English grammar rules, this method attempts to
        correctly pluralise a given word based on the part of speech that it
        follows.

        Parameters
        ----------
        word
            The word to pluralise.
        part_of_speech_for_word
            The part of speech the given word falls under.
        specificity
            The type of the given part of speech.
        preceding_word
            The word that comes before the word to conjugate.

        Returns
        -------
        str
            The noun in its plural or original form.
        """
        if (part_of_speech_for_word.is_a_noun() and (
                preceding_word.is_a_verb() or
                (preceding_word.is_an_amount() and
                    preceding_word.value != "one"))):
            if word.endswith("n"):
                word = re.sub("(a)n$", "en", word)
            elif (not specificity == "people" and
                    word.endswith("y")):
                word = re.sub("y$", "ies", word)
            else:
                word += "s"
        return word
