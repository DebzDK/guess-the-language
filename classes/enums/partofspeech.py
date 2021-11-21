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
