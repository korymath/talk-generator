[![CircleCI](https://circleci.com/gh/korymath/talk-generator.svg?style=svg&circle-token=dcba7d5a9ff7953cff0526e201990c0b811b3aae)](https://circleci.com/gh/korymath/talk-generator)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/korymath/britbot/blob/master/LICENSE.md)

# Talk Powerpoint Generator 
[//]: # "I find puns such as 'AutomaTED' or 'GeneraTED' to be a bit more descriptive than TEDRIC tbh :) -Thomas"


## Description

Software to automatically generate talks, presentations for PowerPoint and/or Keynote.
Their main purpose is for the improvisational comedy format "Improvised TED talk", where the actors have to present an unseen presentation.
This software can be extended to be used for any sort of presentation including for example pecha kucha, etc.

For more details, feel free to see the [project details and technical description.](https://docs.google.com/document/d/1R7v6XELpqCwPH3kZzZHefAY1GiL32_wRhQOT8PpzEys/edit?usp=sharing)

### Example

![Automatically Generated](https://media.giphy.com/media/8gWRbelmFyKoHfwz2Z/giphy.gif)]


## Installation Instructions 

```sh
# Run the setup script from the command line
source setup.sh
```

### Setting up required authentication

Our program relies on certain APIs that require authentication in order to use it.
There are two files that need to be created and place in the folder `data/auth/*`,
namely `reddit.json` and `wikihow.json`:

#### Reddit authentication: `reddit.json`
The file looks like this:
```json
{
  "client_id": "CLIENT_ID_CODE",
  "client_secret": "CLIENT_SECRET",
  "user_agent": "python:https://github.com/korymath/talk-generator:v0.0.1 by /u/REDDIT_USERNAME)"
}
```
You can create this file by following the next steps:
- Create a [Reddit](https://reddit.com) account
- Go to your [App prefenrences](https://ssl.reddit.com/prefs/apps/)
- Pressing "create app"
- Filling in a name and other details
- Filling in the `CLIENT_ID_CODE` above using the id under the name of the app,
the `CLIENT_SECRET` using the text next to `secret` in the app card 
and `REDDIT_USERNAME` with your Reddit username.
- Save it as `data/auth/reddit.json`


#### Wikihow authentication: `wikihow.json`
```json
{
  "username": "WIKIHOW_USERNAME",
  "password": "WIKIHOW_PASSWORD"
}
```
You can create this file by following the next steps:
- Create a [Wikihow](https://wikihow.com) account.
- Fill in `WIKIHOW_USERNAME` with your username, and `WIKIHOW_PASSWORD` with your password.
- Save it as `data/auth/wikihow.json`

### Common Errors/Warnings:

#### BeautifulSoup lxml warning
* Add parser for BeautifulSoup

```sh
sublime venv/lib/python3.6/site-packages/PyDictionary/utils.py
# change:  return BeautifulSoup(requests.get(url).text)
# to: 	   return BeautifulSoup(requests.get(url).text, 'lxml')
```

#### Windows lxml warning
`pip` might complain when installing the `python-pptx` dependency due to a missing the `lxml` dependency.
If this is not resolved automatically, visit [this page](https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml).
On that page, select the right `lxml` version for your platform and Python version (e.g. `cp37` = Python 3.7).

In case installing the dependencies complain about Visual C++ version while resolving the `python-pptx` dependency,
consider installing a version of [Visual Studio](https://docs.microsoft.com/en-us/visualstudio/install/install-visual-studio).

#### Missing mysql.h

If `pip` complains about a missing `mysql.h`, you need to `pip install wheel`,
go to [mysql wheel download]( http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python) to download the wheel
and run `pip install mysqlclient-1.3.8-cp36-cp36m-win_amd64.whl`

## Running the generator

```sh
py run.py --topic cat --num_slides 10
```

### Available arguments

| Argument               | Description               |
| ---------------------- | ------------------------- |
| `topic` | The topic of the generator. This works best if it is a common, well-known noun |
| `num_slides` | The number of slides in the generated presentation |
| `schema` | The presentation schema to use when generating the presentation. Currently, only two modes are implemented, being `default` and `test` (for testing during development) |
| `presenter` | The name that will be present on the first slide. Leave blank for an automatically generated name |
| `output_folder` | The folder to output the generated presentations |
| `save_ppt` | If this flag is true, the generated powerpoint will be saved on the computer in the `output_folder`|
| `open_ppt` | If this flag is true, the generated powerpoint will automatically open after generating|


## Program structure

In this section, we discuss the many parts of this software.

### Powerpoint Template
- `data/powerpoint/template.pptx`: This Powerpoint file contains the powerpoint presentation to start from. 
The interesting part of this file is when opening the model view, as you can edit the slide templates and their
placeholders.

- `slide_templates.py`: This Python module is responsible for filling in the `template.pptx` with values.
There are also functions present which you can give as arguments functions that generates content when given
a `presentation_context` dictionary.
It will then generate the content, and if certain conditions (e.g. originality) are satisfied, it will create and
add a slide to the presentation.

### Presentation Schema elements

- **PresentationSchema**: This class controls the parameters of the powerpoint generator.
It contains information about which slide generators to use, which slide topic generator and
a dictionary `max_allowed_tags` that contains information about how many times slide generators with certain tags
are allowed to generate in one presentation.
We might add different presentation schemas for different types of presentation generators in the future.
The PresentationSchema class can be found in `presentation_schema.py`.

- **SlideGenerator**: This class contains information about how to generate a particular type of slide.
It holds a generating function for this purpose, as well as meta-data. For example, it contains a `weight_function`
to calculate the chance of being used for a certain slide number, a name and tags for the generator, the allowed number 
of elements that have already been used in the presentation and the number of retries the slide generator is allowed
to make in case it fails to generate a slide.
The SlideGenerator class can be found in `presentation_schema.py`.

- **SlideTopicGenerator**: This is type of class that has a `generate_seed(slide_nr)` function, which generates a 
seed for the given slide number, which tends to be based on the topic of the presentation (as entered by the user).
This slide `seed` will then be given to a Slide Generator as an inspiration point for the content of the slide.
There are several types of topic generators, such as a slide topic generator that just returns the presentation topic,
one that gives synonyms and one that makes little side tracks using related concepts on `ConceptNet`

- `presentation_context`: This is an object that is created by the Presentation Schema, containing information about
the topic and presenter of the presentation, the used content and the `seed` for the current slide

### Custom Text Template Language: `text_generator`

We wrote our own custom templated text generation language to easily generate texts.
They're mostly based on Python's `str.format` and Tracery, but come with some extra functionalities
(see also `language_util`)

The template files themselves are stored in `/data/text-templates/*`

#### TemplatedTextGenerator

On construction, this object is given the name of a file that contains a text template on a new line, usually in a 
`.txt` file.
Similar to the build-in `str.format` function, these text templates can contain named variables between curly brackets
`{variable_name}`.
Usually, the `presentation_context` dictionary is used as an argument.
This means that in these text generators `{seed}` will be the variable containing the slide topic seed.
This dictionary can also be extended before generating the text, such that more, custom variables are also possible.

A difference is that our custom language also provides some functions that can be easily called within the template.
If a function returns None, or the variable is not present in the given dictionary, the text generator will keep
retrying to generate until no templates are left.
An example of such a function is `{seed.plural.title}`, which will pluralise the seed, and then apply title casing.

Listed below are some possible functions in our text generation language.
The up-to-date list of function can be found in `text_generator.py`.

| Function               | Description               |
| ---------------------- | ------------------------- |
| `title` | Converts the string to title casing |
| `lower` | Converts the string to lower casing |
| `upper` | Converts the string to upper casing |
| `dashes` | Replaces the spaces of the string with dashes |
| `a` | Adds the "a" article, or "an" if the word starts with a vowel (except *u*) |
| `ing` | Converts a verb to the present participle |
| `plural` | Converts a noun to plural |
| `singular` | Converts a noun to singular |
| `synonym` | Converts the noun to a random synonym |
| `2_to_1_pronouns` | Changes 2nd person pronouns to 1st person pronouns in a sentence (e.g. you->my) |
| `wikihow_action` | Retrieves a random action based on the string using Wikihow |
| `get_last_noun_and_article` | Extracts the last noun from a sentence |
| `conceptnet_location` | Retrieves a location related to the string using Conceptnet |
| `is_noun` | Checks if the string can be a noun |
| `is_verb` | Checks if the string can be a verb |


#### TraceryTextGenerator
Allows the same things `TemplatedTextGenerator` does, but using a
[Tracery grammar](https://github.com/aparrish/pytracery).
This means that the file is saved as a JSON file, and that local variables can be declared, for easily creating a large
possibility space of possible texts.


### Utilities

- `random_util`: This module helps with dealing better with randomness. It has a function to deal with picking from a
list with weighted elements, as well as `choice_optional(list)`, which is like `random.choice`, except it returns None
if the list is empty

- `generator_util`: This module provides lots of utilities for creating generators. Since some content generators
return (image or textual) lists, there are functions for converting them to normal single output generators.
There are also methods for converting methods that only take a string `seed` as input to one that takes a
`presentation_context`, namely `create_seeded_generator(generator)`.
There are also more exotic generators such as weighted generators and walking generators.

- `language_util`: Contains many language functionalities, such as converting to singular/plural, changing tense,
checking part of speech, getting synonyms etc.

- `scraper_util`: Provides some common functionalities for the page scrapers.

- `os_util`: Contains some methods dealing with the operating system, such as saving and checking files.

- `cache_util`: Contains a hashable dictionary class, which is necessary for caching certain functions.


### Content generators 

There are a lot of different services providing content to our generator.
Usually, the content scrapers below are used in `run.py` to craft a real concent generator
used in the slides generators.

- `chart.py`: Generates random powerpoint charts using text templates and random math functions.
- `conceptnet.py`: Explores the graph of related concepts to certain seeds
- `goodreads.py`: Used for retrieving quotes related to a seed
- `google_images.py`: Used for retrieving relevant images for certain seeds (e.g. as background image)
- `inspirobot.py`: Used for retrieving nonsensical quote images
- `reddit.py`: Used for scraping reddit images, as there are many interesting subreddits to scrape images from.
- `shitpostbot.py`: Used for retrieving "interesting"/weird images
- `wikihow.py`: Used for finding related actions to a certain seed.



## Credits

This ``Talk Generator`` is made by [Kory Mathewson](https://github.com/korymath)
and [Thomas Winters](https://github.com/TWinters),
with help from [Piotr Mirowski](https://github.com/piotrmirowski) and Julian Faid.

## License

MIT License. Copyright (c) 2018 Kory Mathewson and Thomas Winters.