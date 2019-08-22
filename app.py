# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import flask

# Take advantage of Plotly's built-in small CSS framework:
# https://codepen.io/chriddyp/pen/bWLwgP.css

# Really useful repo for looking up Dash patterns:
# https://github.com/plotly/dash-recipes/

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

mapbox_access_token = "pk.eyJ1Ijoib3BlbmVlIiwiYSI6ImNqd3NnMnBucjF0ZDQ0YW84MG02aHRpbnkifQ.zHzYA-F7AYOJylDC7wY-Uw"

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# app.config.suppress_callback_exceptions = True

df = pd.read_csv("assets/sf_buildings_clean.csv")

from layouts import app_layout

container_layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

def serve_layout():
    if flask.has_request_context():
        return container_layout
    return html.Div([
        container_layout,
        app_layout
    ])

app.layout = serve_layout

@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return app_layout
    elif pathname == "/building-energy-models":
        return app_layout
    else:
        return "404"


from callbacks import *


if __name__ == "__main__":
    app.run_server(debug=True)
