"""Class for generating random sentences."""
import random
from typing import List, Tuple
from classes.sentence import Sentence
from classes.word import Word
from classes.gamedictionary import GameDictionary
from classes.enums.language import Language
from classes.enums.partofspeech import PartOfSpeech


class SentenceGenerator():
    """A class used to represent a sentence generator.

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
        for count, part_of_speech in enumerate(sentence_structure):
            word, specificity = cls._select_word_for_part_of_speech(
                    part_of_speech, character_limit)
            if count == 0:
                word = word.lower().capitalize()
            words.append(Word(word, part_of_speech, specificity))
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

            if preceding_part_of_speech is PartOfSpeech.CONJUNCTION:
                next_part = cls._get_random_article()
            else:
                try:
                    next_part = random.choice(temp_list_of_choices)
                except IndexError:
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

    @staticmethod
    def _select_word_for_part_of_speech(
            part_of_speech: PartOfSpeech, char_limit: int) -> Word:
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
                part_of_speech)

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
                    if (word_to_add.is_possessive()
                            or word_to_add.is_a_place()
                            or word_to_add.is_a_name()):
                        add_to_blacklist = True

                if (preceding_word.is_an_irregular_verb()
                        and word_to_add.is_an_adverb()):
                    add_to_blacklist = True

                if ((preceding_word.is_an_adjective()
                        or preceding_word.is_a_noun())
                        and word_to_add.is_a_noun()
                        and preceding_word.specificity !=
                        word_to_add.specificity):
                    add_to_blacklist = True

                if (word_to_add.is_a_verb() and preceding_word.is_a_noun()
                        and preceding_word.specificity == "food"
                        and not word_to_add.is_a_being_verb()):
                    add_to_blacklist = True

                if add_to_blacklist:
                    if word_to_add.part_of_speech not in blacklist:
                        blacklist[word_to_add.part_of_speech] = set()
                    blacklist[word_to_add.part_of_speech].add(
                        word_to_add.specificity)

        return (len(blacklist) == 0, blacklist)
