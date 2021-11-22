"""Class for generating random sentences."""
import random
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
