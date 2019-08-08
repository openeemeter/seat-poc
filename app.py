# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

# Take advantage of Plotly's built-in small CSS framework:
# https://codepen.io/chriddyp/pen/bWLwgP.css

# Really useful repo for looking up Dash patterns:
# https://github.com/plotly/dash-recipes/

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

mapbox_access_token = "pk.eyJ1Ijoib3BlbmVlIiwiYSI6ImNqd3NnMnBucjF0ZDQ0YW84MG02aHRpbnkifQ.zHzYA-F7AYOJylDC7wY-Uw"

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_csv("assets/sf_buildings_clean.csv")


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H3(children="SEAT", className="headerSubtitle"),
                        html.H1(
                            children="Efficiency Impact Explorer",
                            className="headerTitle",
                        ),
                        html.H2(
                            children=[
                                html.Span(
                                    children="California", className="locationTitle"
                                ),
                                html.Span(children="/"),
                                html.Span(children="2018", className="yearTitle"),
                            ]
                        ),
                        html.P(
                            children="""
            
                Explore the aggregate impact of energy efficiency projects without
                compromising the privacy of any individual participant.

            """
                        ),
                        html.P(
                            children="""
            
                Data in this proof of concept are synthetic but the privacy protection
                implementation is real, demonstrating the accuracy that can be expected
                in a real-life deployment.

            """
                        ),
                        html.P(
                            children=[
                                """
                
                For more detail on this proof of concept's privacy protection: 

            """,
                                html.A(
                                    "How It Works",
                                    href="https://colab.research.google.com/drive/1DI9v6P3IOYD1QrK99DcpUcAGTMXRHDch",
                                ),
                            ]
                        ),
                    ],
                    className="headerContainer",
                ),
                html.Div(
                    [
                        html.H2(children="Portfolio"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(children="Building Type"),
                                        dcc.RadioItems(
                                            options=[
                                                {
                                                    "label": "All",
                                                    "value": "All Buildings",
                                                },
                                                {
                                                    "label": "Retail Store",
                                                    "value": "Retail Store",
                                                },
                                                {"label": "Office", "value": "Office"},
                                                {"label": "Hotel", "value": "Hotel"},
                                            ],
                                            value="All Buildings",
                                            id="building-type",
                                        ),
                                    ],
                                    className="five columns",
                                ),
                                html.Div(
                                    [
                                        html.H3(children="Energy Conservation Measure"),
                                        dcc.RadioItems(
                                            options=[
                                                {"label": "All", "value": "All ECMS"},
                                                {
                                                    "label": "Building Leakage",
                                                    "value": "Building Leakage",
                                                },
                                                {
                                                    "label": "HVAC System",
                                                    "value": "HVAC System",
                                                },
                                                {
                                                    "label": "HVAC Duct Leakage",
                                                    "value": "HVAC Duct Leakage",
                                                },
                                                {
                                                    "label": "Roof Insulation",
                                                    "value": "Roof Insulation",
                                                },
                                            ],
                                            value="All ECMS",
                                            id="ecm-type",
                                        ),
                                    ],
                                    className="seven columns",
                                ),
                            ],
                            className="u-cf",
                        ),
                        html.H3(children="Custom"),
                        html.P(
                            children="Upload a custom portfolio by filtering the provided building identifiers"
                        ),
                        # html.Div([
                        #     html.A(children="Download Raw Data")
                        # ]),
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div([html.A("Upload Custom Portfolio File")]),
                            style={},
                            disabled=True,
                        ),
                        html.H2("Accuracy", style={"margin-top": "40px"}),
                        html.P(
                            """ 

                Users are allocated a fixed privacy budget. Requesting more accurate
                responses consumes privacy faster than less accurate results. After
                exhausting your budget, no further queries can be made.

            """
                        ),
                        html.Div(
                            [dcc.Slider(min=1, max=20, value=5, id="accuracy-slider")],
                            style={"padding": "15px 0 0 0"},
                        ),
                        html.Div(
                            [
                                html.P(
                                    children=[
                                        html.Span(
                                            "Average Savings Accuracy:",
                                            className="fancyLabel",
                                        ),
                                        html.Span(
                                            "±3%",
                                            className="fancyValue",
                                            id="savings-accuracy",
                                        ),
                                    ]
                                ),
                                html.P(
                                    children=[
                                        "95% confidence interval for Average Savings result. Smaller is better."
                                    ],
                                    className="help",
                                ),
                                html.P(
                                    children=[html.A("More →", id="more-accuracy")],
                                    className="help",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Graph(
                                                    id="accuracy-graph",
                                                    config={"displayModeBar": False},
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                html.P(
                                    children=[
                                        html.Span(
                                            "Privacy Cost:", className="fancyLabel"
                                        ),
                                        html.Span(
                                            "1.2%",
                                            className="fancyValue",
                                            id="privacy-cost",
                                        ),
                                    ]
                                ),
                                html.P(
                                    "Percentage of personal privacy budget this query will consume",
                                    className="help",
                                ),
                            ],
                            style={"margin": "10px 0 0 0"},
                        ),
                        html.Div(
                            [
                                html.Button(
                                    "Submit Query",
                                    id="submit",
                                    className="button-primary",
                                )
                            ],
                            style={"margin": "20px 0"},
                        ),
                    ],
                    className="six columns inputsContainer",
                ),
                html.Div(
                    [
                        html.H2(children="Results"),
                        html.Div(
                            [
                                html.H3("845", id="total-projects"),
                                html.P("Total Projects"),
                            ],
                            className="numberEmphasisChart",
                        ),
                        html.Div(
                            [
                                html.H3("-", id="average-savings"),
                                html.P("Average Savings"),
                                html.P("at 95% confidence", className="help"),
                            ],
                            className="numberEmphasisChart",
                        ),
                        # html.Div([
                        #     html.H3("4%"),
                        #     html.P("Avoided GHG Emissions (Metric Tons)"),
                        # ], className="numberEmphasisChart"),
                    ],
                    className="six columns resultsContainer",
                ),
            ],
            className="six columns",
        ),
        html.Div(
            [
                dcc.Graph(
                    figure=go.Figure(layout=None, data=None),
                    id="map",
                    style={"height": "100vh"},
                )
            ],
            className="six columns",
            style={"margin-left": "0", "width": "50%"},
        ),
        html.Div(id="past-clicks", style={"display": "none"}),
    ],
    className="",
)


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
    if clicks is None or clicks % 2 == 0:
        return {"display": "none"}
    else:
        return {"display": "block"}


if __name__ == "__main__":
    app.run_server(debug=True)
