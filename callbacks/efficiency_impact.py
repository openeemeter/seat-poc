# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from app import app, df, mapbox_access_token

@app.callback(
    [
        dash.dependencies.Output("savings-accuracy", "children"),
        dash.dependencies.Output("accuracy-graph", "figure"),
    ],
    [
        dash.dependencies.Input("accuracy-slider", "value"),
        dash.dependencies.Input("total-projects", "children"),
    ],
)
def update_accuracy(value, N):
    N = int(N)
    e = value / 100.0

    df = 100 / N
    b = df / e

    # Compute error using quantile function of laplace
    error = -b * np.log(2 - 2 * 0.975)
    error *= 2

    # Update accuracy plot
    samples = np.random.laplace(0, b, 5000)
    trace = go.Histogram(
        x=samples,
        opacity=0.7,
        name="Male",
        marker={"line": {"color": "#25232C", "width": 0.2}},
        nbinsx=70,
        customdata=samples,
        histnorm="probability",
    )
    layout = go.Layout(
        xaxis={"title": "Error %", "showgrid": False},
        yaxis={"title": "Probability", "showgrid": False},
        margin={"l": 50, "b": 30, "t": 30, "r": 10},
        height=150,
    )
    figure2 = {"data": [trace], "layout": layout}

    return ("±" + str(round(error, 1)) + "%", figure2)




@app.callback(
    dash.dependencies.Output("privacy-cost", "children"),
    [dash.dependencies.Input("accuracy-slider", "value")],
)
def update_privacy_cost(value):

    # We budget here using Basic Composition
    # Each user has a budget of epsilon = 4 and we assume
    # Parallel Composition with non-overlapping queries.

    e = value / 4

    return str(e) + "%"


def update_map_data(building_type, ecm):

    if building_type == "All Buildings":
        d = df
    else:
        d = df[df["building_type"] == building_type]

    if ecm != "All ECMS":
        d = d[d["ecm"] == ecm]

    N = d.size

    savings = d["savings"].mean()

    # Sample map data
    data = [
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
            center=go.layout.mapbox.Center(lat=df.lat.mean(), lon=df.lng.mean()),
            pitch=0,
            zoom=11,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return str(N), savings, {"data": data, "layout": layout}


@app.callback(
    [
        dash.dependencies.Output("total-projects", "children"),
        dash.dependencies.Output("map", "figure"),
        dash.dependencies.Output("average-savings", "children"),
        dash.dependencies.Output("past-clicks", "children"),
    ],
    [
        dash.dependencies.Input("building-type", "value"),
        dash.dependencies.Input("ecm-type", "value"),
        dash.dependencies.Input("submit", "n_clicks"),
    ],
    [
        dash.dependencies.State("past-clicks", "children"),
        dash.dependencies.State("accuracy-slider", "value"),
        dash.dependencies.State("savings-accuracy", "children"),
    ],
)
def set_building_type(
    selected_building_type,
    selected_ecm,
    num_clicks,
    past_clicks,
    accuracy_value,
    savings_accuracy,
):
    projects, savings, map_figure = update_map_data(
        selected_building_type, selected_ecm
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


@app.callback(
    dash.dependencies.Output("accuracy-graph", "style"),
    [dash.dependencies.Input("more-accuracy", "n_clicks")],
)
def toggle_accuracy_graph(clicks):

    return {"display": "block"}

    if clicks is None or clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {"display": "block"}
