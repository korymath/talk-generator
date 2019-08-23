""" Module providing language-related operations to manipulate strings"""
import logging
import re
import string

import inflect
import nltk

logger = logging.getLogger("talkgenerator")


def check_and_download():
    required_corpus_list = ["tokenizers/punkt", "taggers/averaged_perceptron_tagger"]
    try:
        for corpus in required_corpus_list:
            _check_and_download_corpus(corpus, corpus.split("/")[1])
    except Exception as e:
        print_corpus_download_warning()
        return False

    return True


def _check_and_download_corpus(corpus_fullname, corpus_shortname):
    try:
        nltk.data.find(corpus_fullname)
    except LookupError as le:
        nltk.download(corpus_shortname)


def print_corpus_download_warning():
    corpus_warning = """
    Hmm...
    ---------------------

    We had some trouble downloading the NLTK corpuses.. 
    Try running the following from a command line. This should 
    download the needed packages.. but it might also tell you if 
    there is another issue.

    $ python3 -m nltk.downloader punkt averaged_perceptron_tagger
    """
    logger.warning(corpus_warning)


# Helpers


def _replace_word_one_case(sentence, word, replacement, flags=0):
    return re.sub(
        r"(^|\W)" + word + r"(\W|$)", r"\1" + replacement + r"\2", sentence, flags=flags
    )


def replace_word(sentence, word, replacement):
    lowered = _replace_word_one_case(sentence, word.lower(), replacement.lower())
    upper = _replace_word_one_case(lowered, word.upper(), replacement.upper())
    titled = _replace_word_one_case(upper, word.title(), replacement.title())
    result = _replace_word_one_case(titled, word, replacement, re.I)
    return result


def get_pos_tags(word):
    """ Returns all possible POS tags for a given word according to nltk """
    tags = nltk.pos_tag(nltk.word_tokenize(word))
    tags_strings = [tag[1] for tag in tags]
    # print(word, ":", tags_strings)
    return tags_strings


# Verbs


def get_verb_index(words):
    seen_adverb = False
    for i in range(len(words)):
        tags = get_pos_tags(words[i])
        # Is verb: return
        if "VB" in tags:
            return i
        # Is adverb: return next non adverb
        if "RB" in tags:
            seen_adverb = True
            continue
        # Something following an adverb thats not an adverb? See as verb
        if seen_adverb:
            return i
    return 0


def apply_function_to_verb(action, func):
    words = action.split(" ")
    verb_index = get_verb_index(words)
    first_word = func(words[verb_index])
    if len(words) == 1:
        return first_word
    return (
        " ".join(words[:verb_index])
        + " "
        + first_word
        + " "
        + " ".join(words[verb_index + 1 :])
    ).strip()


def to_present_participle(action):
    return apply_function_to_verb(action, to_ing_form)


# From https://github.com/arsho/46-Simple-Python-Exercises-Solutions/blob/master/problem_25.py
def _make_ing_form(passed_string):
    passed_string = passed_string.lower()
    letter = list(string.ascii_lowercase)
    vowel = ["a", "e", "i", "o", "u"]
    consonant = [c for c in letter if c not in vowel]
    exception = ["be", "see", "flee", "knee", "lie"]

    if passed_string.endswith("ie"):
        passed_string = passed_string[:-2]
        return passed_string + "ying"

    elif passed_string.endswith("e"):
        if passed_string in exception:
            return passed_string + "ing"
        else:
            passed_string = passed_string[:-1]
            return passed_string + "ing"

    elif passed_string.endswith("y") or passed_string.endswith("w"):
        return passed_string + "ing"

    elif (
        len(passed_string) >= 3
        and passed_string[-1] in consonant
        and passed_string[-2] in vowel
        and passed_string[-3] in consonant
    ):
        passed_string += passed_string[-1]
        return passed_string + "ing"
    else:
        return passed_string + "ing"


def to_ing_form(passed_string):
    result = _make_ing_form(passed_string)
    if passed_string.islower():
        return result.lower()
    if passed_string.isupper():
        return result.upper()
    if passed_string.istitle():
        return result.title()
    return result


inflect_engine = inflect.engine()


def is_singular(word):
    return inflect_engine.singular_noun(word) is False


def is_plural(word):
    return bool(inflect_engine.singular_noun(word))


def to_plural(word):
    if is_singular(word):
        if word.startswith("a "):
            word = word[2:]
        return inflect_engine.plural(word)
    return word


def to_singular(word):
    if is_plural(word):
        return inflect_engine.singular_noun(word)
    return word


def add_article(word):
    # TODO: Maybe more checks, some u's cause "an", or some big letters in case it's an abbreviation
    word_lower = word.lower()
    article = "a"
    if (
        word_lower.startswith("a")
        or word_lower.startswith("e")
        or word_lower.startswith("i")
        or word_lower.startswith("o")
    ):
        article = "an"
    return article + " " + word


# Pronouns


def second_to_first_pronouns(sentence):
    sentence = replace_word(sentence, "yours", "mine")
    sentence = replace_word(sentence, "your", "my")
    sentence = replace_word(sentence, "you", "me")
    return sentence


# POS tag checkers

# TODO: These don't work well, but might be useful features in our text generation language
def is_noun(word):
    return "NN" in get_pos_tags(word)


def is_verb(word):
    return "VB" in get_pos_tags(word)


# Special operators


def get_last_noun_and_article(sentence):
    tokens = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(tokens)

    noun = None
    for tag in reversed(tags):
        if "NN" in tag[1]:
            if noun:
                noun = (tag[0] + " " + noun).strip()
            else:
                noun = tag[0]

        # If encountering an article while there is a noun found
        elif bool(noun):
            if "DT" in tag[1] or "PRP$" in tag[1]:
                return tag[0] + " " + noun
            return noun

    return None


def replace_non_alphabetical_characters(text):
    return re.sub(r"[^A-Za-z\s\b -]+", "", text)


def is_vowel(character):
    return character in ["a", "e", "i", "o,", "u"]


def is_consonant(character):
    return not is_vowel(character)
