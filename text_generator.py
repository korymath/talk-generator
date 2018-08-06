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
        # Create a tuple so no templates can accidentally be deleted from the generator
        self._templates = tuple(templates)

    def generate(self, variables_dictionary):
        """ Generates a text from the templates using the given variables dictionary"""
        possible_templates = list(self._templates)
        for i in range(len(possible_templates)):
            template = random.choice(possible_templates)
            if can_format_with(template, variables_dictionary):
                return template.format(**variables_dictionary)
            else:
                # Remove the template from the possible templates list, such that it won
                possible_templates.remove(template)


def can_format_with(template, variables_dictionary):
    """ Checks if the template can be fully formatted by the given variable dictionary without errors"""
    format_variables = get_format_variables(template)
    return set(format_variables) <= set(variables_dictionary.keys())


def get_format_variables(template):
    """ Finds all the names of the variables used in the template """
    matches = re.findall('{(\w+)}', template)
    return matches


def read_lines(file):
    """ Reads all the string lines from a file """
    return [line.rstrip('\n') for line in open(file)]
