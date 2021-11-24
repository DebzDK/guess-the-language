# Testing

## Validator testing

* PEP8 online
    * Initial cursory testing

        As a person who hasn't used Python in about 7 years, preliminary testing was done while in the early stages of development to better understand what to keep in mind while coding.
        
        Many errors, such as those shown below, were encountered and fixed [here](https://github.com/DebzDK/guess-the-language/commits/cursory-pep8online-fixes):
            ![Screenshot of early run.py testing](documentation/screenshots/evidence/early-run-test.png)
        
        Running the contents of [this](https://github.com/DebzDK/guess-the-language/blob/a5062a6b2b17af2659383b60a67ffa681555073a/run.py) file in the PEP8 online tool will produce the above results.

    * Potential non-error errors
        1. The following errors occur in [run.py](https://github.com/DebzDK/guess-the-language/blob/main/run.py#L157) and [requestservice.py](https://github.com/DebzDK/guess-the-language/blob/main/classes/services/requestservice.py#L17):
            ![Screenshot of run.py errors](documentation/screenshots/evidence/run-test.png)
            ![Screenshot of requestservice.py error](documentation/screenshots/evidence/requestservice-class-test.png)

            However, in [PEP 3107](https://legacy.python.org/dev/peps/pep-3107/#syntax), it explains that this is the expected format for funciton annotations that specify a default value and the pystylecode (formerly pep8) tool in Gitpod shows no error on these lines.
            
            ![Screenshot of related PEP 3107 section](documentation/screenshots/evidence/error-conflict-with-pep-3107.png)
            
            This [answer](https://stackoverflow.com/a/38727786) in StackOverflow also supports this.

            For this reason, these errors outlined by the [PEP8 online tool](http://pep8online.com/) can be ignored.

        2. This error occurred in [gamedictionary.py](https://github.com/DebzDK/guess-the-language/blob/main/classes/gamedictionary.py#L25):
            ![Screenshot of gamedictionary.py error](documentation/screenshots/evidence/gamedictionary-class-test.png)

            [PEP 526](https://www.python.org/dev/peps/pep-0526/#class-and-instance-variable-annotations) explains that this is valid form for variable annotations as can be seen here:

            ![Screenshot of relevant PEP 526 section](documentation/screenshots/evidence/pep-526-explanation-in-relation-to-error.png)

            For this reason, this error can also be ignored.

    * All other classes
        * classes/sentence.py - __Sentence()__
            ![Screenshot of translationhelper.py class test](documentation/screenshots/evidence/sentence-class-test.png)
        * classes/sentencegenerator.py - __SentenceGenerator()__
            ![Screenshot of sentencegenerator.py class test](documentation/screenshots/evidence/sentencegenerator-class-test.png)
        * classes/translation.py - __Translation()__
            ![Screenshot of translation.py class test](documentation/screenshots/evidence/translation-class-test.png)
        * classes/word.py - __Word()__
            ![Screenshot of word.py class test](documentation/screenshots/evidence/word-class-test.png)
        * classes/enums/difficulty.py - __Difficulty(Enum)__
            ![Screenshot of difficulty.py class test](documentation/screenshots/evidence/difficulty-class-test.png)
        * classes/enums/inputmode.py - __InputMode(Enum)__
            ![Screenshot of inputmode.py class test](documentation/screenshots/evidence/inputmode-class-test.png)
        * classes/enums/language.py - __Language(Enum)__
            ![Screenshot of language.py class test](documentation/screenshots/evidence/language-class-test.png)
        * classes/enums/partofspeech.py - __PartOfSpeech(Enum)__
            ![Screenshot of partofspeech.py class test](documentation/screenshots/evidence/partofspeech-class-test.png)
        * classes/helpers/translationhelper.py - __TranslationHelper()__
            ![Screenshot of translationhelper.py class test](documentation/screenshots/evidence/translationhelper-class-test.png)