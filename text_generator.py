""" This module helps out with generating text using templates """
import random
import re


class TemplatedTextGenerator:

    def __init__(self, template_file=None, templates_list=None):
        templates = []
        if template_file:
            templates.extend(read_lines(template_file))
        if templates_list:
            templates.extend(templates_list)
        self._templates = templates

    def generate(self, variables_dictionary):
        """ Generates a text from the templates using the given variables dictionary"""
        possible_templates = self._templates.copy()
        for i in range(len(possible_templates)):
            template = random.choice(possible_templates)
            format_variables = get_format_variables(template)
            if set(format_variables) <= set(variables_dictionary.keys()):
                return template.format(**variables_dictionary)
            else:
                possible_templates.remove(template)


def get_format_variables(line):
    matches = re.findall('{(\w+)}', line)
    return matches


def read_lines(file):
    return [line.rstrip('\n') for line in open(file)]
