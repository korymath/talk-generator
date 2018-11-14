virtualenv -p python3 venv
source venv/bin/activate
pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m nltk.downloader wordnet punkt averaged_perceptron_tagger
