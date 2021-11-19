# Guess The Language

'Guess The Language' is a language-guessing game that takes sentences from a .txt file, user input, or auto-generated data and translates them into another language. Its quiz-like fashion aims to introduce people to the beauty of language in a fun way and show how the differences between languages can range from tiny to quite big. The site will be targeted toward people who have an interest in or are curious about languages. This site will also be useful for people who want to see the capability of a translation tool other than Google Translate.

TODO: Add game terminal screenshot

## Requirements

Before jumping into the design process, requirements needed to be specified in order to know exactly what the game should do to meet the assessment criteria. Unlike the previous portfolio projects, the visual output is simply textual and therefore functionality and flow of events is even more so crucial.

![Screenshot of requirements](documentation/screenshots/evidence/requirements.png).

## Design

[Lucidchart](https://www.lucidchart.com/) was used to illustrate the logical flow derived from the requirements in the form of the flowchart shown below.

!['Guess The Language' flowchart](documentation/screenshots/evidence/flow-chart.png)

### Planning and execution

Agile practices were used to carry out this project and documented in Trello [planning/design board](https://trello.com/b/JGCCLlNB/project-planning-design) and [dev board](https://trello.com/b/TsXKTw7W/project-development) and [Github Projects](https://github.com/DebzDK/guess-the-language/projects/1).

*Please note that more task details + resources are available in the Trello boards than in the Github Project page.*

Each board is divided into 3 swimlanes/columns:
* 'To Do' - used to list tasks that are yet to be done
* 'In Progress' - used to list tasks that are currently being carried out
* 'Done' - used to list completed tasks

After defining the status divisions for a task, the indicators for time constraints were defined using 't-shirt sizes'.

![Card labels screenshot from Trello](documentation/screenshots/evidence/task-sizes-and-areas.png)

‘T-shirt sizes’ were defined to provide an estimate for the perceived difficulty of a task and extra labels to further separate tasks by what part of the process they’re related to, i.e. Requirements, Design, Development, and Testing.
The project area labels have been defined as follows:
* ‘Requirements’ - refers to things that are directly taken from or related to the project’s assessment criteria rather than actions derived from a requirements capture process
* 'Design' - refers to steps taken towards the appearance of the website
* 'Development' - refers to steps taken towards the implementation of the website
* 'Testing' - refers to steps taken towards validating the HTML and CSS as well as testing the responsiveness of the website

At this point, user stories were created in order to produce tasks while thinking from a user's perspective.

![Screenshot of first user story made in Trello](documentation/screenshots/evidence/first-user-story.png)

All other user stories follow the same kind of format except for where the user story is self-explanatory of the task.

## Features

Each feature listed below was chosen to provide users with a clear, logical path through the application content in order for this project to achieve its goal.

### Existing features

* Main menu
    * Allows users to see a main menu before starting the game

        TODO: Add GIF once built

        From here, a user can start the game and view/set game options.

* Game options menu
    * Allows users to set options that effect gameplay

        TODO: Add GIF once built

        Option 1 - 'Input mode' - controls what mode of input users will use to input sentences into the game.
        Option 2 - 'Enable hints' - controls where or not users what to receive hints while trying to guess a language.
        Option 3 - 'Difficulty' - controls the amount of languages (and therefore questions) user will encounter per game.

        The free version of the [DeepL Translator](https://www.deepl.com/en/translator) used in the application has a limit of 500,000 characters per month.
        To account for this in the game and allow a reasonable number of games to be played, the following restrictions for sentence character length and the total number of questions per game mode were calculated as follows:

        * Easy (short questions in 'popular' languages) and normal (reasonable-length questions in less 'popular' languages)
            Number of questions: 5
            Max number of characters per sentence: 30
            Total number of games per day: 20

            Total number of characters per month: 5 * 30 * 20 * daysInMonth = 90k - 93k
        
        * Hard - 10 reasonable-length questions in less 'popular' languages
            Number of questions: 10
            Max number of characters per sentence: 40
            Total number of games per day: 10

            Total number of characters per month: 10 * 40 * 10 * daysInMonth = 120k - 124k

        * BEAST - questions in all available languages in the translation API + 5 seconds to answer question
            Number of questions: 26
            Max number of characters per sentence: 20
            Total number of games per day: 10

            Total number of characters per month: 26 * 20 * 10 * daysInMonth = 156k - 161.2k

        These calculations give approx. 471.2k (+ 6 easy games = 498.2k) characters to use over the span of the month which is equal to 1.8k - 1.86k (or 1.98k) playthroughs following the given amount of each game mode.
        This is what will be followed when testing the application while in development so that the limit isn't prematurely exceeded.

        Once the maximum number of requests has been reached, the API will return that information in the form of an error message that will then be displayed to users before the game is exited (if playing) or started (if trying to play).

        *Note: 'popular' languages refers to other European languages that are typically offered as second language options in school and in language learning apps.*

* Game
    * Where the magic happens
        Once a user starts a game, based on the chosen difficulty level and corresponding character limit (as outlined above), they are either prompted for direct input, file input, or presented with auto-generated sentences as input.
        
        The cases are as follows:
        * *User input* - the input is validated per question to ensure it meets the set criteria for translation.

        * *File input* - the same is true here but with the extra step of using auto-generated values in addition to those extracted from the file if there aren't enough viable sentences for translation. If there are more lines of text than required in the file, the rest are ignored.

        * *Auto-generated input* - sentences are validated as they're being generated until the right combination of words fits into the character limit.

        After the appropriate input step is taken, the game proceeds translating the sentence, presenting it to a user in another language, and prompting the user to take a guess.

        Finally, a tally of the total number of correct guesses are displayed and the game ends.

        TODO: Add GIFs for each case once translation work is done

### Future features

* Ability for a user to enter text that isn't English

    The default language to translate from is English because that is my first language and the language of the country where I reside. However, I also speak more-or-less fluent French and am learning Greek so it would be cool to use sentences in these languages in the game.

    The chosen API to run translations does have an optional parameter that, when omitted, allows for language detection so it is possible but there is also the issue of special characters to consider.

* Display of the number of countries in which the translation target language is spoken

    It would be cool to make the game educational by adding a decorator that adds the number of countries where the translation target language is officially spoken after a correct or incorrect answer.

    ```
    You guessed French and the answer was French! French is spoken in approximately [num] countries around the world.
    ```

    Wikipedia has an unofficial public API called ['MediaWiki'](https://www.mediawiki.org/wiki/API:Main_page) and a [wiki](https://en.wikipedia.org/wiki/List_of_languages_by_the_number_of_countries_in_which_they_are_recognized_as_an_official_language) containing this information. The two together, plus some algorithm to extract the desired data for a given language, could've provided this information but it isn't verified and appears to be outdated. I couldn't find another source so I chose not to implement this feature.

* Writing sentences and their translations to a new text file or the existing text file (if one is provided)

    This would allow for some level of persistence for a user who is genuinely interested in languages to keep a log of their translations.

## Languages and technologies used

* Languages
    * [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) - used to create the command line application

* Technologies
    * [DeepL Translator](https://www.deepl.com/en/translator) - used free verison of their API to translate sentences in game
    * [Lucidchart](https://www.lucidchart.com/) - used to create a flow chart of the game's processes
    * [Trello](https://trello.com/) - used to document planning/design and development project progress and steps
    * [Git](https://git-scm.com/) - used for version control
    * [GitHub](https://github.com/) - used for internet hosting and version control through use of Git
    * [Gitpod](https://gitpod.io/) - used as online IDE for software development
        * The terminal was used to create branchs to work on before merging into the main branch. These branches have been preserved for the sake of the assessment, otherwise they would have been deleted after use.
        *Note: initial merges were missing the '--no-ff' flag so commit history was lost*

        TODO: Add screenshot of all GitHub branches for project

## Testing

### Validator testing

* PEP8 online
    * TODO: Add test results once tested

* Accessibility
    * Manual foreground and background colour testing
        * General text
            Contrast Ratio: <b>[21:1](https://webaim.org/resources/contrastchecker/?fcolor=FFFFFF&bcolor=000000)</b>

        * Correct answers
            Contrast Ratio: <b>[15.3:1](https://webaim.org/resources/contrastchecker/?fcolor=00FF00&bcolor=000000)</b>

        * Incorrect answers
            Contrast Ratio: <b>[7.8:1](https://webaim.org/resources/contrastchecker/?fcolor=#FF7070&bcolor=000000)</b>

        * Highlighted menu option text
            Contrast Ratio: <b>[21:1](https://webaim.org/resources/contrastchecker/?fcolor=000000&bcolor=FFFFFF)</b>
        
## Deployment

### Local deployment

Since my work is in a publicly-accesible repository, it can be copied in 3 different ways:

1. Cloning the repository

    <code>git clone https://github.com/DebzDK/guess-the-language.git</code>

1. Forking the repository

    ![Fork repo image](documentation/screenshots/evidence/fork-it.png)

1. Using Gitpod to create a new workspace for the repository with this button: [![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/DebzDK/guess-the-language)

## Credits

### Content

The translations used in this application are thanks to [DeepL Translator](https://www.deepl.com/en/translator).

All other textual content in this application is written in my own words and of my own opinion.

## Acknowledgements

A huge thank you to my secondary school French teacher, Ms. McAlpine, who inspired my love for learning languages and thanks again to my mentor [Tim Nelson](https://github.com/TravelTimN) for his encouragement and constructive feedback!