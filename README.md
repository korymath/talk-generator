# Talk Generator

### Automatically Generated
[![Automatically Generated](https://media.giphy.com/media/x47rKzgCuCaqFqmxSc/giphy.gif)](https://www.youtube.com/watch?v=bhZezzMu7D4 "Automatically Generated")

### Human Generated
[![Human Generated](https://media.giphy.com/media/9FZONXXfCYdnp2eGd1/giphy-downsized-large.gif)](https://www.youtube.com/watch?v=QJ8i8cpVK0E "Human Generated")

## Description

Software to automatically generate talks, presentations for PowerPoint and/or Keynote. These slides can be used for any sort of presentation including TED talks, pecha kucha, etc. 

For more details, feel free to see the [project details and technical description.](https://docs.google.com/document/d/1R7v6XELpqCwPH3kZzZHefAY1GiL32_wRhQOT8PpzEys/edit?usp=sharing)

## Installation Instructions (Mac OSX)

Requires python3, tested on Mac OSX

```sh
# Run the setup script from the command line
./setup.sh
```

## Installation Instructions (Windows)

pip might complain when installing the python-pptx dependency due to a missing the lxml dependency.
If this is not resolved automatically, visit [this page](https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml).
On that page, select the right lxml version for your platform and Python version (e.g. cp37 = Python 3.7).

In case installing the dependencies complain about Visual C++ version while resolving the python-pptx dependency,
consider installing a version of [Visual Studio](https://docs.microsoft.com/en-us/visualstudio/install/install-visual-studio).

## Run

```sh
python3 run.py --topic 'bagels' --num_slides 5 --num_images 1
```

### Common Errors/Warnings:

* Add parser for BeautifulSoup

```sh
sublime venv/lib/python3.6/site-packages/PyDictionary/utils.py
# change:  return BeautifulSoup(requests.get(url).text)
# to: 	   return BeautifulSoup(requests.get(url).text, 'lxml')
```

## References

* [python-pptx](https://github.com/scanny/python-pptx)
* [TED-RNN](https://github.com/samim23/TED-RNN)
* [PptxGenJS](https://gitbrent.github.io/PptxGenJS/docs/quick-start.html)
* [TED Talks Trancripts](https://www.kaggle.com/goweiting/ted-talks-transcript)
* [TED Talks - Complete List](https://data.world/owentemple/ted-talks-complete-list)

## Credits

This ``Talk Generator`` is made by Kory Mathewson and Thomas Winters. With help from Piotr Mirowski and Julian Faid.

## License

MIT License. Copyright (c) 2018 Kory Mathewson and Thomas Winters.