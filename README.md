# keynote-generator

## Install

```sh
python3 -m pip install python-pptx
python3 -m pip install py-thesaurus
python3 -m pip install nltk
python3 -m nltk.downloader wordnet
python3 -m pip install google_images_download
```

### Add parser for BeautifulSoup

```sh
sublime /Users/korymath/Library/Python/2.7/lib/python/site-packages/PyDictionary/utils.py
# modify to: return BeautifulSoup(requests.get(url).text, 'lxml')
```

## Project Draft

* https://docs.google.com/document/d/1R7v6XELpqCwPH3kZzZHefAY1GiL32_wRhQOT8PpzEys/edit#heading=h.ggt0vmwisuu6

## References

* https://github.com/scanny/python-pptx
* https://github.com/samim23/TED-RNN
* https://gitbrent.github.io/PptxGenJS/docs/quick-start.html
* https://gitbrent.github.io/PptxGenJS/docs/usage-pres-create.html