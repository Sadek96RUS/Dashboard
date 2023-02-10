import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output


app = dash.Dash(__name__)

app_layout = html.Div(children=[
    html.H1('Dashboard',
            style={
                'textAlign': 'center'
            }
            ),

    # create drop down
    dcc.Dropdown(options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montreal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
        value='NYC'
    )
    # create Bar graph
])

# Run application
if __name__ == '__main__':
    app.run_server(port=8005)
