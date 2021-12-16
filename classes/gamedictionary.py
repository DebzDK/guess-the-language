"""Class for word lookup based on parts of speech."""
import random
from typing import Dict, List, Tuple
from num2words import num2words
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
            part_of_speech: PartOfSpeech, specificity: str) -> Tuple[str, str]
        Finds and returns a word that meets the given criteria with its part of
        speech type/specificity.
    """

    WORDS: Dict[str, Dict[str, List[str]]] = {
        "articles": {
            "definite": ["the", "this", "that"],
            "indefinite": ["a"]
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
            "people": [
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
            ],
            "food": [
                "delicious",
                "disgusting",
                "yummy",
                "tasty",
                "ok",
                "bad",
                "decent",
                "appetising"
            ]
        },
        "nouns": {
            "place": [
                "London",
                "England",
                "France",
                "Paris",
                "Spain",
                "Madrid",
                "Greece",
                "Athens",
                "Nigeria",
                "Abuja",
                "Kenya",
                "Nairobi",
                "Jamaica",
                "Kingston",
                "Germany",
                "Berlin",
                "Norway",
                "Oslo",
                "Sweden",
                "Stockholm",
                "Russia",
                "Moscow",
                "Ukraine",
                "Kiev",
                "China",
                "Beijing",
                "Nepal",
                "Kathmandu",
                "Japan",
                "Tokyo",
                "India",
                "Indonesia",
                "Jakarta",
                "Thailand",
                "Bangkok",
                "Philippines",
                "Manilla",
                "Venezuela",
                "Caracas",
                "Turkey",
                "Ankara",
                "Iraq",
                "Baghdad",
                "Pakistan",
                "Islamabad",
            ],
            "people": [
                "boy",
                "girl",
                "man",
                "woman",
                "father",
                "step-father",
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
            "name": [
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
                "Xander",
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
            "food": [
                "apple",
                "apricot",
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
            "place": ["at", "in", "to"],
            "associative": ["with", "to"],
        },
        "verbs": {
            "transitive": [
                "eat",
                "hold",
                "play",
                "like",
                "see"
            ],
            "intransitive": [
                "go",
                "come",
            ],
            "being": [
                "am"
            ],
            "possessive": [
                "have"
            ]
        }
    }

    @classmethod
    def search_for_word_by_type(
            cls, part_of_speech: PartOfSpeech,
            desired_type: str,
            excluded_types: Dict[PartOfSpeech, str]) -> Tuple[str, str]:
        """Finds a random word in the WORDS dict that falls under a given part
        of speech.

        Parameters
        ----------
        part_of_speech
            The part of speech that the word falls under.
        desired_type
            The desired type of part of speech to look for, if provided.
        excluded_types
            The types of parts_of_speech to ignore, if provided.

        Returns
        ----------
        str
            A word that matches the given criteria.
        """
        key, specificity = cls._get_search_criteria(part_of_speech)
        random_word = None

        if part_of_speech == PartOfSpeech.ADVERB:
            potential_adjectives = cls.WORDS["adjectives"].get("people")
            adjective = random.choice(potential_adjectives)
            while not random_word:
                random_word = cls._get_adjective_in_adverb_form(adjective)
        elif part_of_speech == PartOfSpeech.AMOUNT:
            number = random.randint(0, 100)
            random_word = cls._get_word_for_number(number)
        else:
            potential_words_by_spec = cls.WORDS.get(key)
            potential_specs = []

            for spec in list(potential_words_by_spec.keys()):
                if not (part_of_speech in excluded_types and
                        specificity in excluded_types[part_of_speech]):
                    potential_specs.append(spec)

            while specificity is None or specificity == "":
                specificity = desired_type or random.choice(potential_specs)

            random_word = random.choice(
                potential_words_by_spec.get(specificity)
            )
        return (random_word, specificity)

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

    @staticmethod
    def _get_adjective_in_adverb_form(adjective: str) -> str:
        """Converts a given adjective to an adverb and returns it.

        Returns
        -------
        str
            The adverb.
        """
        adverb = ""
        last_letter = adjective[-1]
        letter_before_last = adjective[-2]

        if letter_before_last != "l" and last_letter in ("edlsg"):
            adverb = adjective + "ly"
        elif last_letter == "y":
            adverb = adjective[0:-2] + "ily"
        elif last_letter == "c":
            adverb = adjective + "ally"

        return adverb

    @staticmethod
    def _get_word_for_number(number: int) -> str:
        """Gets the number in its word form.

        Returns
        -------
        str
            The number as a word.
        """
        # Use library to convert number to word equivalent
        return num2words(number, lang="en")
