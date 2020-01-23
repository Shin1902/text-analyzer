# import chart_studio.plotly.plotly as py
import plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import json

from modules import color_palette


def create_bar_chart(col_count):


    colors = color_palette.get_colors(len(col_count))
    trace0 = go.Bar(
        x=list(col_count.keys()),
        y=list(col_count.values()),
        marker=dict(color=colors),
    )

    data = [trace0]

    graphJSON = json.dumps(data, cls=py.utils.PlotlyJSONEncoder)
    return graphJSON
