"""Class for generating random sentences."""
import random
from typing import List
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
