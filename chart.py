import random

from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.chart import XL_LEGEND_POSITION
from pptx.enum.chart import XL_TICK_MARK

import text_generator

yes_no_question_generator = text_generator.TraceryTextGenerator(
    'data/text-templates/chart_texts.json', "yes_no_question").generate
funny_yes_no_answer_generator = text_generator.TraceryTextGenerator(
    'data/text-templates/chart_texts.json', "funny_yes_no_answer").generate


# DATA POINTS HELPERS


def add_noise_to_points(max_noise_ratio, datapoints):
    return [add_noise_to_point(max_noise_ratio, point) for point in datapoints]


def add_noise_to_point(max_noise_ratio, datapoint):
    return max(0, datapoint + (datapoint * random.uniform(-max_noise_ratio, max_noise_ratio)))


def normalise_data(datapoints):
    total_sum = sum(datapoints)
    return [datapoint / total_sum for datapoint in datapoints]


# DATA SET CREATION


def create_equal_data_with_outlier_end(size, noise_factor, normal_min, normal_max, outlier_min_size, outlier_max_size):
    # Create data with same number between normal_min and normal_max everywhere
    datapoints = [random.uniform(normal_min, normal_max) for _ in range(0, size)]

    # Make last number an outlier
    datapoints[-1] = random.uniform(outlier_min_size, outlier_max_size)

    # Apply noise
    datapoints = add_noise_to_points(noise_factor, datapoints)

    return datapoints


# CHART TYPES PROPERTIES SETTING
def set_histogram_properties(chart):
    value_axis = chart.value_axis
    value_axis.mayor_tick_mark = XL_TICK_MARK.NONE
    value_axis.minor_tick_mark = XL_TICK_MARK.NONE
    value_axis.has_mayor_gridlines = False
    value_axis.has_minor_gridlines = False
    # value_axis.visible = False

    tick_labels = value_axis.tick_labels
    tick_labels.number_format = "#,##0%"

    return chart


def set_pie_properties(chart):
    chart.legend.position = XL_LEGEND_POSITION.RIGHT
    chart.legend.include_in_layout = False


# CHART TYPES
PIE = XL_CHART_TYPE.PIE, set_pie_properties
PROCENT_HISTOGRAM = XL_CHART_TYPE.COLUMN_CLUSTERED, set_histogram_properties

# CHART DATA GENERATOR

_YES_NO_CHART_TYPES = PIE, PROCENT_HISTOGRAM


def generate_yes_no_large_funny_answer_chart_data(presentation_context):
    title = yes_no_question_generator(presentation_context)

    presentation_context["chart_title"] = title

    categories = ['Yes', 'No', funny_yes_no_answer_generator(presentation_context)]
    series_data = normalise_data(create_equal_data_with_outlier_end(len(categories), .7, 1, 3, 1, 15))

    chart_data = ChartData()
    chart_data.categories = categories
    chart_data.add_series('Answers', series_data)
    return title, chart_data


def generate_yes_no_single_answer_chart_data(presentation_context):
    # TODO: Only one answer, takes up whole answer
    pass


def generate_yes_no_pie(presentation_context):
    title, chart_data = generate_yes_no_large_funny_answer_chart_data(presentation_context)
    type, chart_modifier = random.choice(_YES_NO_CHART_TYPES)
    return title, type, chart_data, chart_modifier
