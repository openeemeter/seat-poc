# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from app import app, mapbox_access_token

from db import building_energy_models_data as data

def update_map_data(selected_building_year):

    d = data

    N = d.size

    savings = 0

    # Sample map data
    map_data = [
        go.Scattermapbox(
            lat=d.lat,
            lon=d.lng,
            mode="markers",
            marker=go.scattermapbox.Marker(size=9, color="rgb(170,79,208)"),
        )
    ]

    # Sample map layout
    layout = go.Layout(
        autosize=True,
        hovermode="closest",
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(lat=d.lat.mean(), lon=d.lng.mean()),
            pitch=0,
            zoom=11,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return str(N), savings, {"data": map_data, "layout": layout}


@app.callback(
    [
        dash.dependencies.Output("bem-total-projects", "children"),
        dash.dependencies.Output("bem-map", "figure"),
        dash.dependencies.Output("bem-average-savings", "children"),
        dash.dependencies.Output("bem-past-clicks", "children"),
    ],
    [
        dash.dependencies.Input("bem-year-built", "value"),
        dash.dependencies.Input("bem-submit", "n_clicks"),
    ],
    [
        dash.dependencies.State("bem-past-clicks", "children"),
        dash.dependencies.State("bem-accuracy-slider", "value"),
        dash.dependencies.State("bem-savings-accuracy", "children"),
    ],
)
def portfolio(
    selected_building_year,
    num_clicks,
    past_clicks,
    accuracy_value,
    savings_accuracy,
):
    projects, savings, map_figure = update_map_data(
        selected_building_year
    )
    N = int(projects)

    if num_clicks is None:
        savings = "-"

    if past_clicks is None:
        past_clicks = 0
    elif past_clicks == "None":
        past_clicks = 0
    else:
        past_clicks = int(past_clicks)

    if past_clicks == num_clicks:
        savings = "-"
    elif savings is not "-":

        # Compute savings with DP

        e = accuracy_value / 100.0

        df = 100 / N
        b = df / e
        noise = np.random.laplace(0, b)

        savings += noise
        savings = "%s%% " % str(round(savings, 1))
        savings += savings_accuracy

    return projects, map_figure, savings, str(num_clicks)

