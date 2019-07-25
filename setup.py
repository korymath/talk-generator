from os import listdir
from os.path import isfile, join

from setuptools import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

# Build a list of text-templates to install
DATA_PATH = 'talkgenerator/data/'
text_templates_path = DATA_PATH + 'text-templates/'
onlyfiles = [f for f in listdir(text_templates_path) if isfile(join(text_templates_path, f))]
all_text_templates = []
for f in onlyfiles:
    all_text_templates.append(text_templates_path + f)

setup(
    name='talkgenerator',
    version='2.0.0',
    description='Automatically generating presentation slide decks.',
    long_description=readme,
    author='Kory Mathewson, Thomas Winters',
    author_email='info@thomaswinters.be',
    url='https://github.com/korymath/talk-generator',
    license=license,
    packages=['talkgenerator'],
    package_dir={'talkgenerator': 'talkgenerator'},
    data_files=[('eval', [DATA_PATH + 'eval/common_words.txt']),
                ('images', [DATA_PATH + 'images/black-transparent.png']),
                ('powerpoint', [DATA_PATH + 'powerpoint/template.pptx']),
                ('prohibited_images', [DATA_PATH + 'prohibited_images/tinypic_removed.png']),
                ('text-templates', all_text_templates),],
    include_package_data=True,
    install_requires=install_requires,
        entry_points={
        'console_scripts': [
            'talkgenerator = talkgenerator.run:main_cli'
        ]
    }
)
