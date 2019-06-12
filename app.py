# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np


# Take advantage of Plotly's built-in small CSS framework:
# https://codepen.io/chriddyp/pen/bWLwgP.css

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

mapbox_access_token = "pk.eyJ1Ijoib3BlbmVlIiwiYSI6ImNqd3NnMnBucjF0ZDQ0YW84MG02aHRpbnkifQ.zHzYA-F7AYOJylDC7wY-Uw"

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_csv("assets/sf_buildings_clean.csv")


app.layout = html.Div([

    html.Div([

        html.Div([
            html.H3(children="SEAT", className="headerSubtitle"),
            html.H1(children="Efficiency Impact Explorer", className="headerTitle"),
            html.H2(children=[
                html.Span(children="California", className="locationTitle"),
                html.Span(children="/"),
                html.Span(children="2018", className="yearTitle")
            ]),

            html.P(children="""
            
                Explore the aggregate impact of energy efficiency projects without
                compromising the privacy of any individual participant.

            """),

            html.P(children="""
            
                Data in this proof of concept are synthetic but the privacy protection
                implementation is real, demonstrating the accuracy that can be expected
                in a real-life deployment.

            """)

        ], className="headerContainer"),

        html.Div([

            html.H2(children="Portfolio"),

            html.Div([

                html.Div([
                    html.H3(children="Building Type"),

                    dcc.RadioItems(
                        options=[
                            {'label': 'All', 'value': 'All Buildings'},
                            {'label': 'Retail Store', 'value': 'Retail Store'},
                            {'label': 'Office', 'value': 'Office'},
                            {'label': 'Hotel', 'value': 'Hotel'}
                        ],
                        value="All Buildings",
                        id="building-type"
                    )
                ], className="five columns"),

                html.Div([
                    html.H3(children="Energy Conservation Measure"),

                    dcc.RadioItems(
                        options=[
                            {'label': 'All', 'value': 'All ECMS'},
                            {'label': 'Building Leakage', 'value': 'Building Leakage'},
                            {'label': 'HVAC System', 'value': 'HVAC System'},
                            {'label': 'HVAC Duct Leakage', 'value': 'HVAC Duct Leakage'},
                            {'label': 'Roof Insulation', 'value': 'Roof Insulation'}
                        ],
                        value="All ECMS",
                        id="ecm-type"
                    )
                ], className="seven columns"),

            ], className="u-cf"),

            html.H3(children="Custom"),

            html.P(children="Upload a custom portfolio by filtering the provided building identifiers"),

            # html.Div([
            #     html.A(children="Download Raw Data")
            # ]),

            dcc.Upload(
                id="upload-data",
                children=html.Div([
                    html.A("Upload Custom Portfolio File")
                ]),
                style={},
                disabled=True
            ),

            html.H2("Accuracy / Epsilon", style={"margin-top": "40px"}),

            html.P(""" 

                Users are allocated a fixed privacy budget. Requesting more accurate
                responses consumes privacy faster than less accurate results. After
                exhausting your budget, no further queries can be made.

            """),

            html.Div([
                dcc.Slider(
                    min=1,
                    max=20,
                    marks={i: str(i) for i in range(1, 21)},
                    value=5,
                    id="accuracy-slider"
                ),
            ], style={"padding": "15px 0"}),

            html.Div([

                html.P(children=[
                    html.Span("Average Savings Accuracy:", className="fancyLabel"),
                    html.Span("±3%", className="fancyValue", id="savings-accuracy")
                ]),

                html.P("95% confidence interval for Average Savings result. Smaller is better.", className="help"),

                html.P(children=[
                    html.Span("Privacy Cost:", className="fancyLabel"),
                    html.Span("1.2%", className="fancyValue", id="privacy-cost")
                ]),

                html.P("Percentage of personal privacy budget this query will consume", className="help")

            ], style={"margin": "40px 0 0 0"}),

            html.Div([
                html.Button("Submit Query", id="submit", className="button-primary"),
            ], style={"margin": "20px 0"})

        ], className="six columns inputsContainer"),

        html.Div([

            html.H2(children="Results"),

            html.Div([
                html.H3("845", id="total-projects"),
                html.P("Total Projects"),
            ], className="numberEmphasisChart"),

            html.Div([
                html.H3("-", id="average-savings"),
                html.P("Average Savings"),
            ], className="numberEmphasisChart"),

            # html.Div([
            #     html.H3("4%"),
            #     html.P("Avoided GHG Emissions (Metric Tons)"),
            # ], className="numberEmphasisChart"),

        ], className="six columns resultsContainer"),


    ], className="six columns"),

    html.Div([
        dcc.Graph(
            figure=go.Figure(
                layout=None,
                data=None
            ),
            id="map",
            style={"height": "100vh"}
        )
    ], className="six columns", style={"margin-left": "0", "width": "50%"}),

    html.Div(id='past-clicks', style={'display': 'none'})

], className="")

@app.callback(
    dash.dependencies.Output("savings-accuracy", "children"),
    [dash.dependencies.Input("accuracy-slider", "value")])
def update_accuracy(value):

    # TODO: compute the error exactly

    # TODO: use the real N
    N = 1639

    e = value / 100.0

    df = 100 / N
    b = df / e
    s = np.random.laplace(0, b, 50000)
    error = np.quantile(s, 0.975)

    return "±" + str(round(error, 1)) + "%"

@app.callback(
    dash.dependencies.Output("privacy-cost", "children"),
    [dash.dependencies.Input("accuracy-slider", "value")])
def update_accuracy(value):

    # This is a bit hand-wavey: the slider value / 100 is epsilon
    # We budget for users to be able to issue 1,000 queries of 
    # epsilon = 0.1 each

    # Probably need to treat this as rho in zCDP and convert to epsilon
    # to account properly.

    e = value / 100.0

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
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9,
                color="rgb(170,79,208)"
            ),
        )
    ]

    # Sample map layout
    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=df.lat.mean(),
                lon=df.lng.mean()
            ),
            pitch=0,
            zoom=11
        ),
        margin = dict(l = 0, r = 0, t = 0, b = 0),
    )

    return str(N), savings, {"data": data, "layout": layout}


@app.callback(
    [
        dash.dependencies.Output("total-projects", "children"),
        dash.dependencies.Output("map", "figure"),
        dash.dependencies.Output("average-savings", "children"),
        dash.dependencies.Output("past-clicks", "children")
    ],
    [
        dash.dependencies.Input("building-type", "value"),
        dash.dependencies.Input("ecm-type", "value"),
        dash.dependencies.Input("submit", "n_clicks")

    ], [
        dash.dependencies.State("past-clicks", "children"),
        dash.dependencies.State("accuracy-slider", "value")
    ])
def set_building_type(selected_building_type, selected_ecm, num_clicks, past_clicks, accuracy_value):
    projects, savings, map_figure = update_map_data(selected_building_type, selected_ecm)

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
        N = int(projects)

        e = accuracy_value / 100.0

        df = 100 / N
        b = df / e
        noise = np.random.laplace(0, b)

        savings += noise
        savings = "%s%%" % str(round(savings, 1))


    return projects, map_figure, savings, str(num_clicks)
    


if __name__ == '__main__':
    app.run_server(debug=True)