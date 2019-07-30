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
# rm -rf talkgenerator.egg-info
# python setup.py clean --all install clean --all
```


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


### Running the generator (development)

```sh
cd talkgenerator
python run.py --topic cat --num_slides 10
```

### Available arguments

| Argument               | Description               |
| ---------------------- | ------------------------- |
| `topic` | The topic of the generator. This works best if it is a common, well-known noun |
| `num_slides` | The number of slides in the generated presentation (*default: 10*) |
| `schema` | The presentation schema to use when generating the presentation. Currently, only two modes are implemented, being `default` and `test` (for testing during development) |
| `presenter` | The name that will be present on the first slide. Leave blank for an automatically generated name |
| `output_folder` | The folder to output the generated presentations (*default: `./output/`*) |
| `save_ppt` | If this flag is true(*default*), the generated powerpoint will be saved on the computer in the `output_folder`|
| `open_ppt` | If this flag is true (*default*), the generated powerpoint will automatically open after generating|
| `parallel` | If this flag is true (*default*), the generator will generate all slides in parallel |



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

## Running the generator as a microservice

Run the generator as a microservice at 0.0.0.0:5687.

`sh python run_web.py`

You can then hit `http://0.0.0.0:5687?topic=sometopic`. This will kick the main.py off.

## Paper

If you would like to refer to this project in academic work, please cite the following paper:

```
@InProceedings{winters2019tedric,
    author="Winters, Thomas
    and Mathewson, Kory W.",
    editor="Ek{\'a}rt, Anik{\'o}
    and Liapis, Antonios
    and Castro Pena, Mar{\'i}a Luz",
    title="Automatically Generating Engaging Presentation Slide Decks",
    booktitle="Computational Intelligence in Music, Sound, Art and Design",
    year="2019",
    publisher="Springer International Publishing",
    address="Cham",
    pages="127--141",
    abstract="Talented public speakers have thousands of hours of practice. One means of improving public speaking skills is practice through improvisation, e.g. presenting an improvised presentation using an unseen slide deck. We present Tedric, a novel system capable of generating coherent slide decks based on a single topic suggestion. It combines semantic word webs with text and image data sources to create an engaging slide deck with an overarching theme. We found that audience members perceived the quality of improvised presentations using these generated slide decks to be on par with presentations using human created slide decks for the Improvised TED Talk performance format. Tedric is thus a valuable new creative tool for improvisers to perform with, and for anyone looking to improve their presentation skills.",
    isbn="978-3-030-16667-0"
}
```

## Program structure

See the [wiki](https://github.com/korymath/talk-generator/wiki/Program-structure) to know more about the inner implementation.


## Tests
There are a lot of tests present in this repository. These `.py` files are prefixed with `test_`, and use the `unittest` module.
They can easily be run all together when using PyCharm by right clicking on `talk-generator` and pressing *Run 'Unittests in talk-generator'*

```sh
. venv/bin/activate
pytest --cov=talkgenerator tests/
```

Test coverage is automatically handled by `codecov`. Tests are automatically run with CircleCI based on the `.yml` file in the `.circleci` directory.


## Credits

This ``Talk Generator`` is made by [Kory Mathewson](https://github.com/korymath)
and [Thomas Winters](https://github.com/TWinters),
with help from [Shaun Farrugia](https://github.com/h0h0h0), [Piotr Mirowski](https://github.com/piotrmirowski) and [Julian Faid](https://github.com/jfaid).

## License

MIT License. Copyright (c) 2018 [Kory Mathewson](https://github.com/korymath)
and [Thomas Winters](https://github.com/TWinters).
