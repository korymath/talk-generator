from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
import random


def generate_test_chart(seed):
    chart_data = ChartData()
    chart_data.categories = ['Yes', 'No']
    chart_data.add_series('Series 1', (random.randint(0,100), random.randint(0,100)))
    return XL_CHART_TYPE.PIE, chart_data
