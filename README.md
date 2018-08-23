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

There are several main parts of this software, namely:

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

TODO: Add explanation of its interface

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

- `cache_util`: Contains a hashable dictionary class, which is necessary for caching certain functions.





## Credits

This ``Talk Generator`` is made by [Kory Mathewson](https://github.com/korymath)
and [Thomas Winters](https://github.com/TWinters),
with help from [Piotr Mirowski](https://github.com/piotrmirowski) and Julian Faid.

## License

MIT License. Copyright (c) 2018 Kory Mathewson and Thomas Winters.