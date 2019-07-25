from setuptools import setup
from setuptools import find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='talkgenerator',
    version='0.0.1',
    description='Automatically generating PowerPoint presentation slide decks',
    long_description=readme,
    author='Kory Mathewson, Thomas Winters',
    author_email='info@thomaswinters.be',
    url='https://github.com/korymath/talk-generator',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True
)
