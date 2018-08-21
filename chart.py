import random

from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE

import text_generator

yes_no_question_generator = talk_subtitle_generator = text_generator.TraceryTextGenerator(
    'data/text-templates/chart_yes_no_question.json').generate


def generate_yes_no_pie(presentation_context):
    title = yes_no_question_generator(presentation_context)

    chart_data = ChartData()
    chart_data.categories = ['Yes', 'No']
    chart_data.add_series('Answers', (random.randint(0, 100), random.randint(0, 100)))
    print(dir(chart_data))

    return title, XL_CHART_TYPE.PIE, chart_data
