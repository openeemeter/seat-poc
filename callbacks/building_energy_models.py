# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from scipy import stats
from app import app, mapbox_access_token

from db import building_energy_models_data as data
from layouts.building_energy_models import outputs


def update_map_data(
    output_id, selected_building_year, number_of_stories, sqft, zipcode
):

    d = data

    # Apply filters
    d = d[d["year_built"].between(*selected_building_year)]
    d = d[d["sqft"].between(*sqft)]
    if number_of_stories:
        d = d[d["floors"].isin(number_of_stories)]
    if zipcode:
        d = d[d["zipcode"].isin(zipcode)]

    N = d.size

    savings = d[output_id].mean()

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
        dash.dependencies.Output("bem-output", "children"),
        dash.dependencies.Output("bem-past-clicks", "children"),
    ],
    [
        dash.dependencies.Input("bem-year-built", "value"),
        dash.dependencies.Input("bem-number-of-stories", "value"),
        dash.dependencies.Input("bem-sqft", "value"),
        dash.dependencies.Input("bem-zipcode", "value"),
        dash.dependencies.Input("bem-submit", "n_clicks"),
        dash.dependencies.Input("bem-output-choice", "value"),
    ],
    [
        dash.dependencies.State("bem-past-clicks", "children"),
        dash.dependencies.State("bem-accuracy-slider", "value"),
        dash.dependencies.State("bem-savings-accuracy", "children"),
    ],
)
def portfolio(
    selected_building_year,
    number_of_stories,
    sqft,
    zipcode,
    num_clicks,
    output_id,
    past_clicks,
    accuracy_value,
    savings_accuracy,
):
    projects, savings, map_figure = update_map_data(
        output_id, selected_building_year, number_of_stories, sqft, zipcode
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

        def private(quantity, value_range):
            e = accuracy_value / 100.0

            df = value_range / N
            b = df / e
            noise = np.random.laplace(0, b)

            quantity += noise
            quantity = "%s " % str(round(quantity, 1))
            quantity += savings_accuracy
            return quantity

        savings = private(savings, outputs[output_id]["value_range"])

    return (projects, map_figure, savings, str(num_clicks))


@app.callback(
    [
        dash.dependencies.Output("bem-savings-accuracy", "children"),
        dash.dependencies.Output("bem-accuracy-graph", "figure"),
    ],
    [
        dash.dependencies.Input("bem-accuracy-slider", "value"),
        dash.dependencies.Input("bem-total-projects", "children"),
        dash.dependencies.Input("bem-output-choice", "value"),
    ],
)
def update_accuracy(value, N, output_id):
    N = int(N)
    e = value / 100.0

    df = outputs[output_id]["value_range"] / N
    b = df / e

    # Compute error using quantile function of laplace
    error = -b * np.log(2 - 2 * 0.975)
    error *= 2

    # Update accuracy plot
    xs = np.linspace(-error, error, 5000)
    ys = stats.laplace.pdf(xs, loc=0, scale=b)

    trace = go.Scatter(x=xs, y=ys, mode="lines")
    layout = go.Layout(
        xaxis={"title": "Error", "showgrid": False},
        yaxis={
            "title": "Probability",
            "showgrid": False,
            "ticks": "",
            "showticklabels": False,
        },
        margin={"l": 50, "b": 30, "t": 30, "r": 10},
        height=150,
    )
    figure2 = {"data": [trace], "layout": layout}

    return ("±" + str(round(error, 2)), figure2)


@app.callback(
    dash.dependencies.Output("bem-output-label", "children"),
    [dash.dependencies.Input("bem-output-choice", "value")],
)
def handle_output_choice(output_id):
    output = outputs[output_id]
    return (output["label"],)


@app.callback(
    dash.dependencies.Output("bem-privacy-cost", "children"),
    [dash.dependencies.Input("bem-accuracy-slider", "value")],
)
def update_privacy_cost(value):

    # We budget here using Basic Composition
    # Each user has a budget of epsilon = 4 and we assume
    # Parallel Composition with non-overlapping queries.

    e = value / 4

    return str(e) + "%"
