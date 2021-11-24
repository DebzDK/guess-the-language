# Guess The Language

'Guess The Language' is a language-guessing game that takes sentences from a .txt file, user input, or auto-generated data and translates them into another language. Its quiz-like fashion aims to introduce people to the beauty of language in a fun way and show how the differences between languages can range from tiny to quite big. The site will be targeted toward people who have an interest in or are curious about languages. This site will also be useful for people who want to see the capability of a translation tool other than Google Translate.

![Screenshot of 'Guess The Language'](documentation/screenshots/evidence/title.png)

## Requirements

Before jumping into the design process, requirements needed to be specified in order to know exactly what the game should do to meet the assessment criteria.

Unlike the previous portfolio projects, the visual output is simply textual and therefore functionality and flow of events is even more so crucial.

The following functional requirements were decided on:
1. The game must present the user with a logo and/or welcome message.
2. The game must display a navigable main menu.
3. The game must allow a user to choose how they want to play.
4. The game must allow a user to quit the game at any time before the end of the game.
5. The game must display the user's score in the form of: `You guessed {correct_answers}/{total_num_of_questions} correctly!`.
6. The game must display the correct answer after every wrong answer.
7. The game must allow a user to have a total of 3 hints if enabled.

## Design

### Logical flow

[Lucidchart](https://www.lucidchart.com/) was used to illustrate the logical flow derived from the requirements in the form of the flowchart shown below.

!['Guess The Language' flowchart](documentation/screenshots/evidence/flow-chart.png)

### Encapsulation

While implementing the basic functions of the game, it was necessary to start thinking about how to model the various components of the game in order to separate concerns. This was, initially, a difficult task until I remembered a tool that would help with breaking down the processes - a [Unified Modeling Language (UML)](https://en.wikipedia.org/wiki/Unified_Modeling_Language) diagram.

After this brainwave, a structural UML diagram, a.k.a [a class diagram](https://en.wikipedia.org/wiki/Class_diagram#General_relationship), was created as shown below.

![Initial class diagram for 'Guess The Language'](documentation/screenshots/evidence/original-class-diagram.png)

TODO: Add screenshot of implemented classes

### Coding practices

To ensure that the project code is up to standard, the following PEP rules were adhered to:

* [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) - for best code style practices (i.e. layout, naming conventions, comments, etc.) and programming recommendations on function and variable annotations
* [PEP 257 -- Docstring Conventions](https://www.python.org/dev/peps/pep-0257/) - for general rules on docstrings
* [NumPy Style Guide](https://numpydoc.readthedocs.io/en/latest/format.html) - for a more detailed explanation of what goes where in docstrings, using [this](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html) specifically as an example to follow
* [PEP 3107 -- Function Annotations](https://www.python.org/dev/peps/pep-3107/) - for a specific way to specify function information and avoid confusion
* [PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-3107/) - also for purposes of clarity (although provisional)
* [PEP 526 -- Syntax for Variable Annotations](https://www.python.org/dev/peps/pep-0526/) - also for purposes of clarity

### Planning and execution

Agile practices were used to carry out this project and documented in Trello [planning/design board](https://trello.com/b/JGCCLlNB/project-planning-design) and [dev board](https://trello.com/b/TsXKTw7W/project-development) and [Github Projects](https://github.com/DebzDK/guess-the-language/projects/1).

*Please note that more task details + resources are available in the Trello boards than in the Github Projects page.*

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

Each feature listed below was chosen to provide users with a clear, logical path through the application content in order for this project to achieve its goal and its functional requirements.

### Existing features

* Main menu
    * Allows users to see a main menu before starting the game

        ![Screenshot of main menu](documentation/screenshots/evidence/main-menu.png)

        From here, a user can start the game and view/set game options.

* Game options menu
    * Allows users to set options that effect gameplay

        ![Game options menu GIF](documentation/screenshots/evidence/game-options.gif)

        * Option 1 - 'Input mode' - controls what mode of input users will use to input sentences into the game.
        * Option 2 - 'Difficulty' - controls the amount of languages (and therefore questions) user will encounter per game.
        * Option 3 - 'Enable hints' - controls where or not users what to receive hints while trying to guess a language.

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
            Number of questions: 25
            Max number of characters per sentence: 20
            Total number of games per day: 10

            Total number of characters per month: 25 * 20 * 10 * daysInMonth = 144k - 148.8k

        These calculations give max approx. 458.8k (+ 9 easy games = 499.3k) characters to use over the span of the month which is equal to 1.8k - 1.86k (or 1.98k) playthroughs following the given amount of each game mode.
        This is what will be followed when testing the application while in development so that the limit isn't prematurely exceeded.

        Once the maximum number of requests has been reached, the API will return that information in the form of an error message that will then be displayed to users before the game is exited (if playing) or started (if trying to play).

        *Please note: 'popular' languages refers to other European languages that are typically offered as second language options in school and in language learning apps, such as Duolingo.*

* Game
    * Where the magic happens
        * Mechanics

            Once a user starts a game, based on the chosen difficulty level and corresponding character limit (as outlined above), they are either prompted for direct input, file input, or presented with auto-generated sentences as input.
            
            After the appropriate input step is taken, the game proceeds to translating the sentence, presenting it to a user in another language, and prompting the user to take a guess. This repeats until the total number of questions for a game has been reached.

            Finally, a tally of the total number of correct guesses are displayed and the game ends.
            
            The cases are as follows:
            * *User input* - the input is validated per question to ensure it meets the set criteria for translation.

                ![GIF of user-input game mode](documentation/screenshots/evidence/user-input.gif)

            * *File input* - the same is true here but with the extra step of using auto-generated values in addition to those extracted from the file if there aren't enough viable sentences for translation. If there are more lines of text than required in the file, the rest are ignored.
                
                ![GIF of user-input game mode](documentation/screenshots/evidence/file-input.gif)

            * *Auto-generated input* - sentences are validated as they're being generated until the right combination of words fits into the character limit.
            
                TODO: Add GIF once auto-generation is fully working

        * Available translation languages

            As mentioned before, Duolingo was referred to in regards to what could be used to classify 'popular' languages and ultimately was used as a guideline to categorise what languages should play for which difficulty levels:
                ![Screenshot of Duolingo with annotations](documentation/screenshots/evidence/duolingo-languages.png)

            *Note: Duolingo offers more languages than this. The ones that aren't used in the game have been removed from this image.*
                
            * Easy - Spanish, French, Japanese, German & Italian (5)

            * Normal - Chinese, Russian, Brazilian Portuguese, Dutch & Swedish (5)

            * Hard - Greek, Polish, Danish, Finnish, Romanian, Czech, Hungarian + 3 more languages from the DeepL Translator API (10)

            * Beast - All of the above + the remaining languages from the API (Total = 24)

            *The other languages offered by the API are Latvian, Lithuanian, Portuguese (Portugal), Slovenian, Slovak and English but English has been excluded since that is the language we assume to be translating from.*

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
    * [EZGIF](https://ezgif.com/) - used to create the GIFs used in this README
    * [Lucidchart](https://www.lucidchart.com/) - used to create a flow chart of the game's processes
    * [DeepL Translator](https://www.deepl.com/en/translator) - used to translate sentences in game
    * [Regex101](https://regex101.com/) - used to create and test the regular expressions used in game for validation
    * [num2words](https://github.com/savoirfairelinux/num2words#readme) - used library to convert numbers to their word equivalent
    * [Requests](https://docs.python-requests.org/en/latest/) - used library to make HTTP requests to DeepL Translator API
    * [StackOverflow](https://stackoverflow.com/) - used to find answers to coding issues, specifically [how to get coloured text](https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal), [understand the python equivalent of getters and setters](https://stackoverflow.com/questions/2627002/whats-the-pythonic-way-to-use-getters-and-setters), and [the purpose of \__init__\.py](https://stackoverflow.com/questions/448271/what-is-init-py-for)
    * [w3schools](https://www.w3schools.com/) - used to find Python functions to complete tasks
    * [Trello](https://trello.com/) - used to document planning/design and development project progress and steps
    * [Git](https://git-scm.com/) - used for version control
    * [GitHub](https://github.com/) - used for internet hosting and version control through use of Git
    * [Gitpod](https://gitpod.io/) - used as online IDE for software development
        * The terminal was used to create branchs to work on before merging into the main branch. These branches have been preserved for the sake of the assessment, otherwise they would have been deleted after use.

        TODO: Add screenshot of all GitHub branches for project

## Testing

Evidence for this section has been placed in its own .md file which can be found [here](https://github.com/DebzDK/guess-the-language/blob/main/TESTING.md).
        
## Deployment

The application was deployed via [Heroku](https://www.heroku.com/) using the steps listed below:

1. In Heroku, click 'New' then 'Create app'.

    ![Screeshot of deployment step 1](documentation/screenshots/evidence/deployment-step-1.png)

1. Name the app and select your closest region.

    ![Screeshot of deployment step 2](documentation/screenshots/evidence/deployment-step-2.png)

1. Connect to Github and find the guess-the-language project.

    ![Screeshot of deployment step 3](documentation/screenshots/evidence/deployment-step-3.png)

1. Set up configuration variables and build packages.

    ![Screeshot of deployment step 4](documentation/screenshots/evidence/deployment-step-4.png)

1. Choose either 'Enable Automatic Deployments' or 'Deploy' for manual deployments.

    *Note: Automatic deployments were enabled for this project.*

    ![Screeshot of deployment step 5](documentation/screenshots/evidence/deployment-step-5.png)

The live link can be found here - https://guess-the-language.herokuapp.com/

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