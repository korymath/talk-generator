virtualenv -p python3 venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m nltk.downloader wordnet
