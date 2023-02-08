import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

air_data = pd.read_csv('airline_data.csv')

app = dash.Dash(__name__)
app.layout = html.Div(children=[html.H1('Flight delay time stat', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),
                                html.Div(['Input Year: ', dcc.Input(id='input-year:', value='2010',
                                                                    type='number', style={'height': '35px', 'font-size': '30'})],
                                         style={'font-size': 30}),
                                html.Br(),
                                html.Br(),
                                html.Div([
                                    html.Div(dcc.Graph(id='carrier-plot')),
                                    html.Div(dcc.Graph(id='weather-plot'))
                                ], style={'display': 'flex'}),
                                html.Div([
                                    html.Div(dcc.Graph(id='nas-plot')),
                                    html.Div(dcc.Graph(id='security-plot'))
                                ], style={'display': 'flex'}),
                                html.Div(dcc.Graph(id='late-plot'),
                                         style={'Width': '65%'})
                                ])


def compute_info(air_data, enter_year):
    df = air_data[air_data['Year'] == int(enter_year)]
    avg_car = df.groupby(['Month', 'Reporting_Airline'])[
        'CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])[
        'WeatherDelay'].mean().reset_index()
    avg_nas = df.groupby(['Month', 'Reporting_Airline'])[
        'NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])[
        'SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])[
        'LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_nas, avg_sec, avg_late


@app.callback([
    Output(component_id='carrier-plot', component_property='figure'),
    Output(component_id='weather-plot', component_property='figure'),
    Output(component_id='nas-plot', component_property='figure'),
    Output(component_id='security-plot', component_property='figure'),
    Output(component_id='late-plot', component_property='figure'),
],
    Input(component_id='input-year:', component_property='value'))
def get_graph(enter_year):
    avg_car, avg_weather, avg_nas, avg_sec, avg_late = compute_info(
        air_data, enter_year)
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay',
                          color='Reporting_Airline', title='Average carrier delay time (min)')
    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay',
                          color='Reporting_Airline', title='Average weather delay time (min)')
    nas_fig = px.line(avg_nas, x='Month', y='NASDelay',
                      color='Reporting_Airline', title='Average NAS delay time (min)')
    sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay',
                      color='Reporting_Airline', title='Average security delay time (min)')
    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay',
                       color='Reporting_Airline', title='Average late aircraft delay time (min)')

    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]


if __name__ == '__main__':
    app.run_server(port=8901)
