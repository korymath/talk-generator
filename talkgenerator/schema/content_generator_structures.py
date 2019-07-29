"""
This file contains structures that are helpful for certain content generators, but not general enough for generator_util
"""
import os
import random

from talkgenerator.util.generator_util import SeededGenerator, BackupGenerator, InvalidImagesRemoverGenerator
from talkgenerator.util.generator_util import ExternalImageListGenerator
from talkgenerator.util.generator_util import FromListGenerator

from talkgenerator.sources import goodreads, text_generator, reddit, wikihow


# = TEXT GENERATORS=

def create_templated_text_generator(filename):
    actual_file = os_util.to_actual_file(filename)
    return text_generator.TemplatedTextGenerator(actual_file).generate


def create_tracery_generator(filename, main="origin"):
    actual_file = os_util.to_actual_file(filename)
    return text_generator.TraceryTextGenerator(actual_file, main).generate


# GOODREAD QUOTES
class GoodReadsQuoteGenerator(object):
    def __init__(self, max_quote_length):
        self._max_quote_length = max_quote_length

    def __call__(self, presentation_context):
        def generator(seed):
            return [quote for quote in goodreads.search_quotes(seed, 50) if len(quote) <= self._max_quote_length]

        return FromListGenerator(SeededGenerator(generator))(presentation_context)


# REDDIT
from talkgenerator.util import os_util


def create_reddit_image_generator(*name):
    reddit_generator = RedditImageGenerator("+".join(name))
    return BackupGenerator(reddit_generator.generate, reddit_generator.generate_random)


class RedditLocalImageLocationGenerator(object):
    def __init__(self, subreddit):
        self._subreddit = subreddit

    def __call__(self, url):
        filename = "downloads/reddit/" + self._subreddit + "/" + os_util.get_file_name(url)
        return os_util.to_actual_file(filename)


class RedditImageSearcher(object):
    def __init__(self, subreddit):
        self._subreddit = subreddit

    def __call__(self, seed):
        results = reddit.search_subreddit(
            self._subreddit,
            str(seed) + " nsfw:no (url:.jpg OR url:.png OR url:.gif)")
        if bool(results):
            return [post.url for post in results]


class RedditImageGenerator:
    def __init__(self, subreddit):
        self._subreddit = subreddit

        self._generate = ExternalImageListGenerator(
            SeededGenerator(RedditImageSearcher(self._subreddit)),
            RedditLocalImageLocationGenerator(self._subreddit)
        )

    def generate(self, presentation_context):
        return self._generate(presentation_context)

    def generate_random(self, _):
        return self.generate({"seed": ""})


# SHITPOSTBOT
class ShitPostBotURLGenerator(object):
    def __init__(self):
        pass

    def __call__(self, url):
        return os_util.to_actual_file("downloads/shitpostbot/{}".format(
            os_util.get_file_name(url)))


# UNSPLASH

class UnsplashURLGenerator(object):
    def __init__(self):
        pass

    def __call__(self, url):
        return os_util.to_actual_file("downloads\\unsplash\\{}.jpg".format(os_util.get_file_name(os.path.dirname(url))))


# ABOUT ME

_about_me_facts_grammar = "data/text-templates/about_me_facts.json"
job_description_generator = create_tracery_generator(_about_me_facts_grammar, "job_description")
country_description_generator = create_tracery_generator(_about_me_facts_grammar, "country_description")


def _apply_country_prefix(country_name):
    if random.uniform(0, 1) < 0.55:
        return country_name
    return country_description_generator() + country_name


class CountryPrefixApplier(object):
    def __init__(self):
        pass

    def __call__(self, x):
        return _apply_country_prefix(x[0]), x[1]


def _apply_job_prefix(job_name):
    if random.uniform(0, 1) < 0.55:
        return job_name
    return job_description_generator() + ": " + job_name


class JobPrefixApplier(object):
    def __init__(self):
        pass

    def __call__(self, x):
        return _apply_job_prefix(x[0]), x[1]


# SPLITTER

class SplitCaptionsGenerator(object):
    def __init__(self, generator):
        self._generator = generator

    def __call__(self, presentation_context):
        line = self._generator(presentation_context)
        parts = line.split("|")
        return parts


# BOLD STATEMENT

bold_statement_templated_file = os_util.to_actual_file('data/text-templates/bold_statements.txt')
bold_statement_templated_generator = create_templated_text_generator(bold_statement_templated_file)


def generate_wikihow_bold_statement(presentation_context):
    seed = presentation_context["seed"]
    template_values = presentation_context
    related_actions = wikihow.get_related_wikihow_actions(seed)
    if related_actions:
        action = random.choice(related_actions)
        template_values.update({'action': action.title(),
                                'seed': seed})

    return bold_statement_templated_generator(template_values)


# GOOGLE
def generate_google_image_generator(generator):
    return FromListGenerator(InvalidImagesRemoverGenerator(SeededGenerator(generator)))
