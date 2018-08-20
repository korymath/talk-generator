""" Module providing language-related operations to manipulate strings"""
import re
import string

import inflect
import nltk
from nltk.corpus import wordnet as wn

import random_util


# Helpers

def _replace_word_one_case(sentence, word, replacement, flags=0):
    return re.sub('(^|\W)' + word + '(\W|$)', r'\1' + replacement + r'\2', sentence, flags=flags)


def replace_word(sentence, word, replacement):
    lowered = _replace_word_one_case(sentence, word.lower(), replacement.lower())
    upper = _replace_word_one_case(lowered, word.upper(), replacement.upper())
    titled = _replace_word_one_case(upper, word.title(), replacement.title())
    result = _replace_word_one_case(titled, word, replacement, re.I)
    return result


# Verbs

def to_present_participle_first_word(action):
    words = action.split(" ")
    first_word = to_ing_form(words[0])
    if len(words) == 1:
        return first_word
    return first_word + " " + " ".join(words[1:])


def to_present_participle(text):
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)

    result = ""
    seen_verb = False
    for tag in pos_tags:
        if not seen_verb and tag[1] == 'VB':
            seen_verb = True
            result += to_ing_form(" " + tag[0])
        result += " " + tag[0]
    return result.strip()


# From https://github.com/arsho/46-Simple-Python-Exercises-Solutions/blob/master/problem_25.py
def _make_ing_form(passed_string):
    passed_string = passed_string.lower()
    letter = list(string.ascii_lowercase)
    vowel = ['a', 'e', 'i', 'o', 'u']
    consonant = [c for c in letter if c not in vowel]
    exception = ['be', 'see', 'flee', 'knee', 'lie']

    if passed_string.endswith('ie'):
        passed_string = passed_string[:-2]
        return passed_string + 'ying'

    elif passed_string.endswith('e'):
        if passed_string in exception:
            return passed_string + 'ing'
        else:
            passed_string = passed_string[:-1]
            return passed_string + 'ing'

    elif passed_string.endswith('y'):
        return passed_string + 'ing'

    elif passed_string[-1] in consonant and passed_string[-2] in vowel and passed_string[-3] in consonant:
        passed_string += passed_string[-1]
        return passed_string + 'ing'
    else:
        return passed_string + 'ing'


def to_ing_form(passed_string):
    result = _make_ing_form(passed_string)
    if passed_string.islower():
        return result.lower()
    if passed_string.isupper():
        return result.upper()
    if passed_string.istitle():
        return result.title()
    return result


def get_definitions(word):
    """Get definitions of a given topic word."""
    print('******************************************')
    # Get definition
    word_senses = wn.synsets(word)
    definitions = {}
    for ss in word_senses:
        definitions[ss.name()] = ss.definition()
    print('{} definitions for "{}"'.format(len(definitions), word))
    return definitions


def get_synonyms(word):
    """Get all synonyms for a given word."""
    word_senses = wn.synsets(word)
    all_synonyms = []
    for ss in word_senses:
        all_synonyms.extend(
            [x.lower().replace('_', ' ') for x in ss.lemma_names()])
    all_synonyms.append(word)
    all_synonyms = list(set(all_synonyms))
    return all_synonyms


def get_random_synonym(word):
    return random_util.choice_optional(get_synonyms(word))


def get_relations(word):
    """Get relations to given definitions."""
    rels = {}
    all_rel_forms = []
    all_perts = []
    all_ants = []

    word_senses = wn.synsets(word)
    for ss in word_senses:
        ss_name = ss.name()
        rels[ss_name] = {}
        for lem in ss.lemmas():
            lem_name = lem.name()
            rels[ss_name][lem_name] = {}
            rel_forms = [x.name() for x in lem.derivationally_related_forms()]
            rels[ss_name][lem_name]['related_forms'] = rel_forms
            all_rel_forms.extend(rel_forms)

            perts = [x.name() for x in lem.pertainyms()]
            rels[ss_name][lem_name]['pertainyms'] = perts
            all_perts.extend(perts)

            ants = [x.name() for x in lem.antonyms()]
            rels[ss_name][lem_name]['antonyms'] = ants
            all_ants.extend(ants)

    print('******************************************')
    print('{} derivationally related forms'.format(len(all_rel_forms)))
    print('******************************************')
    print('{} pertainyms'.format(len(all_perts)))
    print('******************************************')
    print('{} antonyms'.format(len(all_ants)))
    return rels


inflect_engine = inflect.engine()


def is_singular(word):
    return inflect_engine.singular_noun(word) is False


def is_plural(word):
    return bool(inflect_engine.singular_noun(word))


def to_plural(word):
    if is_singular(word):
        return inflect_engine.plural(word)
    return word


def to_singular(word):
    if is_plural(word):
        return inflect_engine.singular_noun(word)
    return word


def add_article(word):
    # TODO: Maybe more checks, some u's cause "an", or some big letters in case it's an abbreviation
    word = word.lower()
    article = "a"
    if word.startswith("a") or word.startswith("e") or word.startswith("i") or word.startswith("o"):
        article = "an"
    return article + " " + word


def second_to_first_pronouns(sentence):
    sentence = replace_word(sentence, "yours", "mine")
    sentence = replace_word(sentence, "your", "my")
    sentence = replace_word(sentence, "you", "me")
    return sentence
