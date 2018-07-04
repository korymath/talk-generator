# Talk Generator

## Installation Instructions (Mac OSX)

Requires python3, tested on Mac OSX

```sh
# Run the setup script from the command line
./setup.sh
```

## Installation Instructions (Windows)

Pip might complain when installing the python-pptx dependency due to a missing the lxml dependency.
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

## Project Details Draft

* https://docs.google.com/document/d/1R7v6XELpqCwPH3kZzZHefAY1GiL32_wRhQOT8PpzEys/edit#heading=h.ggt0vmwisuu6

## References

* https://github.com/scanny/python-pptx
* https://github.com/samim23/TED-RNN
* https://gitbrent.github.io/PptxGenJS/docs/quick-start.html
* https://gitbrent.github.io/PptxGenJS/docs/usage-pres-create.html

## Credits

This ``Talk Generator`` is made by Kory Mathewson and Thomas Winters.

## License

MIT License. Copyright (c) 2018 Kory Mathewson and Thomas Winters.