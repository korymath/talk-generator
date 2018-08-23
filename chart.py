import random

from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.chart import XL_LABEL_POSITION
from pptx.enum.chart import XL_TICK_MARK

import conceptnet
import text_generator

yes_no_question_generator = text_generator.TraceryTextGenerator(
    'data/text-templates/chart_texts.json', "yes_no_question").generate
location_question_generator = text_generator.TraceryTextGenerator(
    'data/text-templates/chart_texts.json', "location_question").generate
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

def _set_pie_label_positions(chart, series, chart_data, label_position):
    chart.plots[0].has_data_labels = True
    for i in range(len(chart_data.categories)):
        point = series.points[i]
        value = series.values[i]
        point.data_label.text_frame.text = "{} ({:.0%})".format(chart_data.categories[i].label,
                                                                value)
        if label_position:
            point.data_label.position = label_position


def set_histogram_properties(chart, chart_data):
    value_axis = chart.value_axis
    value_axis.mayor_tick_mark = XL_TICK_MARK.NONE
    value_axis.minor_tick_mark = XL_TICK_MARK.NONE
    value_axis.has_mayor_gridlines = False
    value_axis.has_minor_gridlines = False
    # value_axis.visible = False

    tick_labels = value_axis.tick_labels
    tick_labels.number_format = '0%'

    return chart


def set_pie_properties(chart, chart_data):
    if chart and chart_data:
        chart.has_legend = False
        chart.has_title = False

        # Data points
        series = chart.series[0]
        # Check if there are small values that can't be contained on the pie piece
        label_position = XL_LABEL_POSITION.OUTSIDE_END if any(
            t < 0.10 for t in series.values) else XL_LABEL_POSITION.CENTER

        # set labels to contain category and value
        _set_pie_label_positions(chart, series, chart_data, label_position)


def set_doughnut_properties(chart, chart_data):
    if chart and chart_data:
        chart.has_legend = False
        series = chart.series[0]
        _set_pie_label_positions(chart, series, chart_data, None)


# CHART TYPES
PIE = XL_CHART_TYPE.PIE, set_pie_properties
PROCENT_HISTOGRAM = XL_CHART_TYPE.COLUMN_CLUSTERED, set_histogram_properties
DOUGHNUT = XL_CHART_TYPE.DOUGHNUT, set_doughnut_properties

# CHART DATA GENERATOR

_YES_NO_CHART_TYPES = PIE, PROCENT_HISTOGRAM, DOUGHNUT


def generate_yes_no_large_funny_answer_chart_data(presentation_context):
    title = yes_no_question_generator(presentation_context)

    presentation_context["chart_title"] = title

    categories = ['Yes', 'No', funny_yes_no_answer_generator(presentation_context)]
    series_data = normalise_data(create_equal_data_with_outlier_end(len(categories), .7, 1, 2.5, 1, 20))

    chart_data = ChartData()
    chart_data.categories = categories
    chart_data.add_series("", series_data)
    return title, chart_data


def generate_location_data(presentation_context):
    seed = presentation_context["seed"]
    title = location_question_generator(presentation_context)

    presentation_context["chart_title"] = title

    related_locations = conceptnet.get_weighted_related_locations(seed)

    if related_locations:
        print(related_locations)
        related_locations = conceptnet.remove_duplicates(related_locations)
        related_locations = conceptnet.remove_containing(related_locations, seed)
        random.shuffle(related_locations)

        related_locations = related_locations[0:random.randint(2, 5)]
        print(related_locations)
        categories = [location[1] for location in related_locations]
        values = [float(location[0]) ** 2 for location in related_locations]

        if len(categories) == 0:
            return None
        series_data = normalise_data(values)

        chart_data = ChartData()
        chart_data.categories = categories
        chart_data.add_series("", series_data)
        return title, chart_data


# FULL CHART GENERATORS

def generate_yes_no_pie(presentation_context):
    title, chart_data = generate_yes_no_large_funny_answer_chart_data(presentation_context)
    chart_type, chart_modifier = random.choice(_YES_NO_CHART_TYPES)
    return title, chart_type, chart_data, chart_modifier


def generate_location_pie(presentation_context):
    result = generate_location_data(presentation_context)
    if result:
        title, chart_data = result
        chart_type, chart_modifier = random.choice(_YES_NO_CHART_TYPES)
        return title, chart_type, chart_data, chart_modifier
