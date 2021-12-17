"""Class for getting game hints."""


class HintService():
    """Class for getting game hints.

    Attributes
    ----------
    HINTS_FOR_LANGS: Dict[str, List[str]]
        A dictionary of hints by their relevant language.
    counter: int
        The index of the current hint.

    Methods
    -------
    get_next_hint(lang_code: str, index: int) -> str
        Gets the next hint for the given language.
    reset_counter():
        Rests counter to 0.
    """

    HINTS_FOR_LANGS = {
        "BG": [
            (
                "The originating country of this language is in the Balkans, "
                "specifically\n southeastern Europe."
            ),
            (
                "The originating country is famous for its folklore, "
                "opera singers, and rose oil."
            ),
            "The capital of the originating country is Sofia.",
        ],
        "CS": [
            "The originating country of this language is in central Europe.",
            (
                "The originating country is famous for its mouth-blown art "
                "glass and crystal."
            ),
            "The capital of the originating country is Prague.",
        ],
        "DA": [
            "The originating country of this language is Scandinavian.",
            (
                "The originating country is famous for being the birthplace of"
                "author Hans Christian\n Andersen, as well as high quality"
                "architecture."
            ),
            "The capital of the originating country is Copenhagen.",
        ],
        "DE": [
            "The originating country of this language is in western Europe.",
            (
                "The originating country is famous for sausages and beer and "
                "is the birthplace of\n Albert Einstein."
            ),
            "The capital of the originating country is Berlin.",
        ],
        "EL": [
            (
                "The originating country of this language is in southeastern "
                "Europe."
            ),
            (
                "The originating country is famous for its mythology and "
                "being the birthplace\n of democracy."
            ),
            "The capital of the originating country is Athens.",
        ],
        "EN_GB": [],
        "ES": [
            "The originating country of this language is in Western Europe.",
            (
                "The originating country is famous for its delicious food, ",
                "passionate dancing,\n and easy-going culture."
            ),
            "The capital of the originating country is Madrid.",
        ],
        "ET": [
            "The originating country of this language is in Northern Europe.",
            (
                "The originating country is famous for its dense woods ",
                "and the charming\n history of its capital."
            ),
            "The capital of the originating country is Tallinn.",
        ],
        "FI": [
            (
                "The originating country of this language is in northern "
                "Europe, bordering\n Sweden, Norway, and Russia."
            ),
            (
                "The originating country is famous for being one of the "
                "happiest countries\n in the world."
            ),
            "The capital of the originating country is Helsinki.",
        ],
        "FR": [
            "The originating country of this language is in western Europe.",
            "The originating country is famous for its wine and cheese.",
            "The capital of the originating country is Paris.",
        ],
        "HU": [
            "The originating country of this language is in central Europe",
            (
                "The originating country is famous for its national dish: "
                "goulash."
            ),
            "The capital of the originating country is Budapest.",
        ],
        "IT": [
            (
                "The originating country of this language is in the Balkans, "
                "specifically\n southeastern Europe."
            ),
            (
                "The originating country is famous for its leaning tower and "
                "being the\n birthplace of pizza and pasta."
            ),
            "The capital of the originating country is Rome.",
        ],
        "JA": [
            "The originating country of this language is in Asia.",
            (
                "The originating country is famous for its cherry blossoms and"
                " being home\n to Mount Fuji."
            ),
            "The capital of the originating country is Tokyo.",
        ],
        "LT": [
            (
                "The originating country of this language is in the Baltic "
                "region of Europe."
            ),
            (
                "The originating country's flag colours are: yellow, green and"
                " red."
            ),
            "The capital of the originating country is Vilnius.",
        ],
        "LV": [
            "The originating country of this language is in eastern Europe.",
            "The originating country's flag colours are: red and white.",
            "The capital of the originating country is Riga.",
        ],
        "NL": [
            (
                "The originating country of this language is in northwestern "
                "Europe."
            ),
            (
                "The originating country is famous for its canals, windmills, "
                "tulips."
            ),
            "The capital of the originating country is Amsterdam.",
        ],
        "PL": [
            "The originating country of this language is in central Europe.",
            (
                "The originating country is famous for its salt mines "
                "and being the\n birthplace of Andrzej Sapkowski, the author "
                "of the Witcher series."
            ),
            "The capital of the originating country is Warsaw.",
        ],
        "PT-PT": [
            "The originating country of this language is in southern Europe.",
            (
                "The originating country is famous for its soccer legends, "
                "fado music,\n and port wine."
            ),
            "The capital of the originating country is Lisbon.",
        ],
        "PT-BR": [
            "The originating country of this language is in South America.",
            (
                "The originating country is famous for its iconic festivals, "
                "soccer legends,\n and for being the location of the Amazon "
                "Rainforest."
            ),
            "The capital of the originating country is Brasilia.",
        ],
        "RO": [
            (
                "The originating country of this language is in southeastern "
                "Europe."
            ),
            (
                "The originating country is famous for Translyvania and the "
                "story of Dracula."
            ),
            "The capital of the originating country is Bucharest.",
        ],
        "RU": [
            (
                "The originating country of this language spans eastern Europe"
                " and northern Asia."
            ),
            (
                "The originating country is famous for having the world's "
                "longest railway,\n being the world's largest nation, and "
                "being the birthplace\n of writers such as Leo Tolstoy and "
                "Fyodor Dostoevsky."
            ),
            "The capital of the originating country is Moscow.",
        ],
        "SK": [
            "The originating country of this language is in central Europe.",
            (
                "The originating country is famous for having the highest "
                "concentration\n of castles in the world and is home to the "
                "Andy Warhol Museum of Modern Art."
            ),
            "The capital of the originating country is Bratislava.",
        ],
        "SL": [
            "The originating country of this language is in central Europe.",
            (
                "The originating country is famous for being home to some of",
                " the best ski\n resorts in Europe."
            ),
            "The capital of the originating country is Ljubljana.",
        ],
        "SV": [
            "The originating country of this language is Scandinavian.",
            "The originating country is famous for ABBA and IKEA.",
            "The capital of the originating country is Stockholm.",
        ],
        "ZH": [
            "The originating country of this language is in Asia.",
            (
                "The originating country is famous for its traditions, "
                "martial arts\n and architectural wonders, such as the Great "
                "Wall."
            ),
            "The capital of the originating country is Beijing.",
        ]
    }

    @classmethod
    def get_next_hint(
            cls, lang_code: str, index: int) -> str:
        """Gets the next hint for a given language.

        Returns
        -------
        str
            The next hint.
        """
        if (lang_code in cls.HINTS_FOR_LANGS and
                index < len(cls.HINTS_FOR_LANGS[lang_code])):
            hint = cls.HINTS_FOR_LANGS[lang_code][index]
        else:
            hint = "No more hints."
        return hint
