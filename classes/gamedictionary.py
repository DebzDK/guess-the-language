"""Class for word lookup based on parts of speech."""
from typing import Dict, List


class GameDictionary():
    """Class for looking up words, like a dictionary.

    Attributes
    ----------
    WORDS: Dict[str, List[str]]
        A dictionary of words by their identifying part of speech
        and part of speech type/specificity.
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
