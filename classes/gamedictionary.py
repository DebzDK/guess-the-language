"""Class for word lookup based on parts of speech."""
import random
from typing import Dict, List
from classes.enums.partofspeech import PartOfSpeech


class GameDictionary():
    """Class for looking up words, like a dictionary.

    Attributes
    ----------
    WORDS: Dict[str, List[str]]
        A dictionary of words by their identifying part of speech
        and part of speech type/specificity.

    Methods
    -------
    search_for_word_by_type(
            part_of_speech: PartOfSpeech, specificity: str) -> str
        Finds and returns a word that meets the given criteria.
    """

    WORDS: Dict[str, Dict[str, List[str]]] = {
        "articles": {
            "definite": ["the", "this", "that"],
            "indefinite": ["a", "an"]
        },
        "pronouns": {
            "personal": ["I", "we", "you", "he", "she", "they", "it"],
            "object": ["me", "us", "you", "him", "her", "it", "them"],
            "possessive": ["mine", "ours", "yours", "theirs"],
            "reflexive": [
                "myself",
                "ourselves",
                "yourself",
                "himself",
                "herself",
                "itself",
                "themselves"
            ]
        },
        "adjectives": {
            "possessive": ["mine", "ours", "yours", "his", "hers", "theirs"],
            "compliment": [
                "attentive",
                "articulate",
                "beautiful",
                "considerate",
                "cute",
                "extraordinary",
                "fun",
                "funny",
                "handsome",
                "kind",
                "marvellous",
                "nice",
                "pretty",
                "strong",
                "stunning",
                "spontaneous",
                "suave",
                "thoughtful",
                "well-dressed",
                "wonderful",
            ]
        },
        "nouns": {
            "places": [],
            "people": [
                "boy",
                "girl",
                "man",
                "woman",
                "father",
                "step-father"
                "dad",
                "step-dad",
                "mother",
                "mum",
                "sister",
                "step-sister",
                "brother",
                "step-brother",
                "aunt",
                "uncle",
                "grandmother",
                "grandfather",
                "grandma",
                "grandpa",
                "cousin",
                "boyfriend",
                "girlfriend"
                ],
            "names": [
                "Alberto",
                "Alex",
                "Agatha",
                "Ann",
                "Ben",
                "Betty",
                "Bernadette",
                "Bucky",
                "Cathy",
                "Chris",
                "Connor",
                "Deborah",
                "Donald",
                "Drew",
                "Emma",
                "Ethel",
                "Enrique",
                "Eugene",
                "Fiona",
                "Frank",
                "Gail",
                "George",
                "Harrison",
                "Hilda",
                "Hilary",
                "Ian",
                "Isaac",
                "Isabelle",
                "Ivanka",
                "Jay",
                "Jermaine",
                "Joyce",
                "Jacqueline",
                "Kim",
                "Kate",
                "Kevin",
                "Kieran",
                "Laura",
                "Lenard",
                "Luke",
                "Liz",
                "Max"
                "Matthew",
                "Maria",
                "Martha",
                "Norbit",
                "Nolan",
                "Natalia",
                "OJ",
                "Oliver",
                "Olga",
                "Owen",
                "Paddington",
                "Paul",
                "Penelope",
                "Pippa",
                "Rachel",
                "Raphael",
                "Rufus",
                "Ruth",
                "Sam",
                "Sabrina",
                "Simon",
                "Stephanie",
                "Tabitha",
                "Taylor",
                "Tim",
                "Tyler",
                "Ulric",
                "Ursula",
                "Veronica",
                "Vince",
                "Vera",
                "Wanda",
                "Wayne",
                "William",
                "Wilhemina",
                "Xander"
                "Xavier",
                "Xena",
                "Yolanda",
                "Yennifer",
                "Zachariah",
                "Zach",
                "Zane",
                "Zara",
                "Zeke",
                "Zelda",
            ],
            "fruits": [
                "apple",
                "apricots",
                "banana",
                "blueberry",
                "cherry",
                "kiwi",
                "jackfruit",
                "lychee",
                "mango",
                "orange",
                "papaya",
                "pear",
                "raspberry",
                "strawberry",
                "watermelon"
            ]
        },
        "conjuctions": {
            "common": [
                "and",
                "so",
                "but",
                "because",
            ]
        },
        "prepositions": {
            "comparitive": ["than"],
            "place": ["at", "in", "on"],
            "assosiative": ["with"],
        },
        "verbs": {
            "action": [
                "go",
                "come",
                "sit",
                "stand",
                "see",
                "run"
            ],
            "irregular": [
                "is",
                "have"
            ],
        }
    }

    @classmethod
    def search_for_word_by_type(cls, part_of_speech: PartOfSpeech) -> str:
        """Finds a random word in the WORDS dict that falls under a given part
        of speech.

        Parameters
        ----------
        part_of_speech
            The part of speech that the word falls under.

        Returns
        ----------
        str
            A word that matches the given criteria.
        """
        key, specificity = cls._get_search_criteria(part_of_speech)

        potential_words_by_spec = cls.WORDS.get(key)

        if not specificity:
            specificity = random.choice(list(potential_words_by_spec.keys()))

        return random.choice(potential_words_by_spec.get(specificity))

    @staticmethod
    def _get_search_criteria(part_of_speech: PartOfSpeech) -> tuple:
        """Retrieves search criteria for a given part of speech.

        Parameters
        ----------
        part_of_speech
            The enum representation for a part of speech.

        Returns
        ----------
        tuple
            Key and specificity that make up the search criteria.
        """
        # In order to match with a key in our dictionary, we must split the
        # PartOfSpeech enum's name value.
        # For values that contain a '_', this will give us a specificity with
        # which to further narrow the search.
        criteria = part_of_speech.value.split("_")

        # We need to reverse it to get the correct order
        criteria.reverse()

        # Unpacks criteria into corresponding variables and handles case for
        # parts of speech that have no specificity in their key
        key, specificity = criteria if len(criteria) == 2 else (
                criteria[0], None)

        return (key + "s", specificity)
