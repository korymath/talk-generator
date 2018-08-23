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





## Credits

This ``Talk Generator`` is made by [Kory Mathewson](https://github.com/korymath)
and [Thomas Winters](https://github.com/TWinters),
with help from [Piotr Mirowski](https://github.com/piotrmirowski) and Julian Faid.

## License

MIT License. Copyright (c) 2018 Kory Mathewson and Thomas Winters.