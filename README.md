# Talk Powerpoint Generator
[![CircleCI](https://circleci.com/gh/korymath/talk-generator.svg?style=svg&circle-token=dcba7d5a9ff7953cff0526e201990c0b811b3aae)](https://circleci.com/gh/korymath/talk-generator)
[![codecov](https://codecov.io/gh/korymath/talk-generator/branch/master/graph/badge.svg?token=gqkCyuXop0)](https://codecov.io/gh/korymath/talk-generator)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/korymath/britbot/blob/master/LICENSE.md)

## Description

Software to automatically generate talks, presentations for PowerPoint and/or Keynote. Their main purpose is for the improvisational comedy format "Improvised TED talk", where the actors have to present an unseen presentation. This software can be extended to be used for any sort of presentation including for example pecha kucha, etc.

## Demo

For a demo of this generator, please visit [the online demo page](https://shaun.lol/), a platform created by Shaun Farrugia to give easier access to this talk generator.

### Example

![Automatically Generated](https://media.giphy.com/media/8gWRbelmFyKoHfwz2Z/giphy.gif)]

## Installation Instructions

```sh
# Run the setup script from the command line
source setup.sh
# Optionally install using setup.py
# python setup.py install
```

## Running the generator (development)

```sh
cd talkgenerator
python run.py --topic cat --num_slides 10
```

### Tests
There are a lot of tests present in this repository. These `.py` files are prefixed with `test_`, and use the `unittest` module. They can easily be run all together when using PyCharm by right clicking on `talk-generator` and pressing *Run 'Unittests in talk-generator'*

```sh
. venv/bin/activate
pytest --cov=talkgenerator tests/
```

Test coverage is automatically handled by `codecov`. Tests are automatically run with CircleCI based on the `.yml` file in the `.circleci` directory.


### Setting up Required API Keys

Our program relies on certain APIs that require authentication in order to use it. Create a file named `.env` (don't forget the period) in your project directory.

```
# Reddit Authentication
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT="" #use quotes here

# Wikihow Authentication
WIKIHOW_USERNAME=
WIKIHOW_PASSWORD=

# Unsplash Authentication
UNSPLASH_ACCESS_KEY=
UNSPLASH_SECRET_KEY=
UNSPLASH_REDIRECT_URI=
UNSPLASH_CODE=

# OPTIONAL: If you want to save to Amazon S3, define your params here
AWS_TALK_BUCKET_KEY=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
```

#### Reddit authentication: Getting your keys

Get your Reddit authentication keys by following these steps.
- Create a [Reddit](https://reddit.com) account
- Go to your [App preferences](https://ssl.reddit.com/prefs/apps/)
- Pressing "create app"
- Filling in a name and other details
- name: 'talk-generator', 'script', description: 'talk-generator', about url: 'https://github.com/korymath/talk-generator', redirect url: 'https://github.com/korymath/talk-generator'
- Open `.env`
- Fill in the `REDDIT_CLIENT_ID` above using the id under the name of the app,
the `REDDIT_CLIENT_SECRET` using the text next to `secret` in the app card.

The `REDDIT_USERAGENT` can be set to "python:https://github.com/korymath/talk-generator:v0.0.1 by /u/REDDIT_USERNAME)" and replace the REDDIT_USERNAME with your Reddit username.

#### Wikihow authentication: Getting your keys

You can create this file by following the next steps:
- Create a [Wikihow](https://wikihow.com) account.
- Open `.env`
- Fill in `WIKIHOW_USERNAME` with your username, and `WIKIHOW_PASSWORD` with your password.


#### Unsplash authentication: Getting your keys

TODO(korymath)

### Available arguments

These are the available runtime arguments that you can pass to the talk-generator. 

| Argument               | Description               |
| ---------------------- | ------------------------- |
| `topic` | The topic of the generator. This works best if it is a common, well-known noun |
| `num_slides` | The number of slides in the generated presentation (*default: 10*) |
| `schema` | The presentation schema to use when generating the presentation. Currently, only two modes are implemented, being `default` and `test` (for testing during development) |
| `presenter` | The name that will be present on the first slide. Leave blank for an automatically generated name |
| `output_folder` | The folder to output the generated presentations (*default: `./output/`*) |
| `save_ppt` | If this flag is true(*default*), the generated powerpoint will be saved on the computer in the `output_folder`|
| `open_ppt` | If this flag is true (*default*), the generated powerpoint will automatically open after generating|


### Common Errors/Warnings:

#### prawcore.exceptions.ResponseException: received 401 HTTP response
From the [Reddit API documentation](https://github.com/reddit-archive/reddit/wiki/OAuth2#retrieving-the-access-token), it sounds like the 401 error is given when your client id/secret are incorrect. Are you using the correct values from the app page?

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

## Docker Instructions (optional)

*slaps the hood of the container* Yep this bad boy runs on [Docker](https://www.docker.com/products/docker-desktop).


### Building the Image

Build the image, and tag it as talkgen.

`docker build -t talkgen .`

### Running the Image

Run the image tagged as talkgen. The container /output directory maps to your
current working directory.

`docker run --env-file .env -v ``pwd``/output:/output talkgen run.py --open_ppt false`

Reasonable defaults have been provided. To override, simply pass the command-line parameter. Here we are overriding the the topic and number of slides.

`docker run --env-file .env -v ``pwd``/output:/output talkgen run.py --topic 'climate change' --num_slides 12 --open_ppt false`

* be sure that open_ppt is false when running as a docker process.


## Running the generator as a microservice

Run the generator as a microservice at 0.0.0.0:5687.

`sh python run_web.py`

You can then hit `http://0.0.0.0:5687?topic=sometopic`. This will kick the main.py off.

## Program structure

In this section, we discuss the many parts of this software.

### Powerpoint Template
- `data/powerpoint/template.pptx`: This Powerpoint file contains the powerpoint presentation to start from. The interesting part of this file is when opening the model view, as you can edit the slide templates and their
placeholders.

- `slide_templates.py`: This Python module is responsible for filling in the `template.pptx` with values. There are also functions present which you can give as arguments functions that generates content when given a `presentation_context` dictionary. It will then generate the content, and if certain conditions (e.g. originality) are satisfied, it will create and add a slide to the presentation.

### Presentation Schema elements

- **PresentationSchema**: This class controls the parameters of the powerpoint generator. It contains information about which slide generators to use, which slide topic generator and a dictionary `max_allowed_tags` that contains information about how many times slide generators with certain tags are allowed to generate in one presentation. We might add different presentation schemas for different types of presentation generators in the future. The PresentationSchema class can be found in `presentation_schema.py`.

- **SlideGenerator**: This class contains information about how to generate a particular type of slide. It holds a generating function for this purpose, as well as meta-data. For example, it contains a `weight_function` to calculate the chance of being used for a certain slide number, a name and tags for the generator, the allowed number of elements that have already been used in the presentation and the number of retries the slide generator is allowed to make in case it fails to generate a slide. The SlideGenerator class can be found in `presentation_schema.py`.

- **SlideTopicGenerator**: This is type of class that has a `generate_seed(slide_nr)` function, which generates a seed for the given slide number, which tends to be based on the topic of the presentation (as entered by the user). This slide `seed` will then be given to a Slide Generator as an inspiration point for the content of the slide. There are several types of topic generators, such as a slide topic generator that just returns the presentation topic, one that gives synonyms and one that makes little side tracks using related concepts on `ConceptNet`

- `presentation_context`: This is an object that is created by the Presentation Schema, containing information about
the topic and presenter of the presentation, the used content and the `seed` for the current slide

### Custom Text Template Language: `text_generator`

We wrote our own custom templated text generation language to easily generate texts. They're mostly based on Python's `str.format` and Tracery, but come with some extra functionalities (see also `language_util`)

The template files themselves are stored in `/data/text-templates/*`

#### TemplatedTextGenerator

On construction, this object is given the name of a file that contains a text template on a new line, usually in a `.txt` file. Similar to the build-in `str.format` function, these text templates can contain named variables between curly brackets `{variable_name}`. Usually, the `presentation_context` dictionary is used as an argument. This means that in these text generators `{seed}` will be the variable containing the slide topic seed. This dictionary can also be extended before generating the text, such that more, custom variables are also possible.

A difference is that our custom language also provides some functions that can be easily called within the template. If a function returns None, or the variable is not present in the given dictionary, the text generator will keep retrying to generate until no templates are left. An example of such a function is `{seed.plural.title}`, which will pluralise the seed, and then apply title casing.

Listed below are some possible functions in our text generation language. The up-to-date list of function can be found in `text_generator.py`.

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
Allows the same things `TemplatedTextGenerator` does, but using a [Tracery grammar](https://github.com/aparrish/pytracery). This means that the file is saved as a JSON file, and that local variables can be declared, for easily creating a large possibility space of possible texts.


### Utilities

- `random_util`: This module helps with dealing better with randomness. It has a function to deal with picking from a list with weighted elements, as well as `choice_optional(list)`, which is like `random.choice`, except it returns None if the list is empty

- `generator_util`: This module provides lots of utilities for creating generators. Since some content generators return (image or textual) lists, there are functions for converting them to normal single output generators. There are also methods for converting methods that only take a string `seed` as input to one that takes a `presentation_context`, namely `create_seeded_generator(generator)`. There are also more exotic generators such as weighted generators and walking generators.

- `language_util`: Contains many language functionalities, such as converting to singular/plural, changing tense, checking part of speech, getting synonyms etc.

- `scraper_util`: Provides some common functionalities for the page scrapers.

- `os_util`: Contains some methods dealing with the operating system, such as saving and checking files.

- `cache_util`: Contains a hashable dictionary class, which is necessary for caching certain functions.

### Content generators

There are a lot of different services providing content to our generator. Usually, the content scrapers below are used in `run.py` to craft a real concent generator used in the slides generators.

- `chart.py`: Generates random powerpoint charts using text templates and random math functions.
- `conceptnet.py`: Explores the graph of related concepts to certain seeds
- `goodreads.py`: Used for retrieving quotes related to a seed
- `google_images.py`: Used for retrieving relevant images for certain seeds (e.g. as background image)
- `inspirobot.py`: Used for retrieving nonsensical quote images
- `reddit.py`: Used for scraping reddit images, as there are many interesting subreddits to scrape images from.
- `shitpostbot.py`: Used for retrieving "interesting"/weird images
- `wikihow.py`: Used for finding related actions to a certain seed.

#### Prohibited images
Sometimes, certain content providers return a default image when no image is found for that url (usually when an image got deleted). These types of images are stored in our repository in `data/images/prohibited/*`. This folder gets automatically scanned, and all images in the generated presentation are compared to images from this folder, to ensure that none gets added to the final presentation.

## Credits

This ``Talk Generator`` is made by [Kory Mathewson](https://github.com/korymath)
and [Thomas Winters](https://github.com/TWinters),
with help from [Shaun Farrugia](https://github.com/h0h0h0), [Piotr Mirowski](https://github.com/piotrmirowski) and [Julian Faid](https://github.com/jfaid).

## License

MIT License. Copyright (c) 2018 [Kory Mathewson](https://github.com/korymath)
and [Thomas Winters](https://github.com/TWinters).
