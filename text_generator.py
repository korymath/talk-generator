""" This module helps out with generating text using templates """
import random
import re


class TemplatedTextGenerator:

    def __init__(self, template_file):
        self._templates = read_lines(template_file)

    def generate(self, variables_dictionary):
        """ Generates a text from the templates using the given variables dictionary"""
        possible_templates = self._templates.copy()
        for i in range(len(possible_templates)):
            template = random.choice(possible_templates)
            format_variables = get_format_variables(template)
            if set(format_variables) <= set(variables_dictionary.keys()):
                return template.format(variables_dictionary)
            else:
                possible_templates.remove(template)


def get_format_variables(line):
    matches = re.findall('{(\w+)}', line)
    print(matches)
    return matches


def read_lines(file):
    return [line.rstrip('\n') for line in open(file)]
