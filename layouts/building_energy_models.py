# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from .nav import nav

from db import building_energy_models_data as data

max_year_built = data["year_built"].max()
min_year_built = data["year_built"].min()
year_built_selector = html.Div(
    [
        html.H3(children="Year Built"),
        dcc.RangeSlider(
            id="bem-year-built",
            count=1,
            min=min_year_built,
            max=max_year_built,
            step=1,
            value=[min_year_built, max_year_built],
        ),
    ]
)

building_type_selector = html.Div(
    [
        html.H3(children="Building Type"),
        dcc.Dropdown(
            options=[
                {"label": "Hotel", "value": "NYC"},
                {"label": "Retail Store", "value": "MTL"},
                {"label": "Office", "value": "SF"},
            ],
            multi=True,
            value="MTL",
        ),
    ]
)


floors = [{"label": x, "value": x} for x in data["floors"].sort_values().unique()]
number_of_stories_selector = html.Div(
    [html.H3(children="Number of Stories"), dcc.Dropdown(options=floors, multi=True)]
)

min_sqft = data["sqft"].min()
max_sqft = data["sqft"].max()
sqft_selector = html.Div(
    [
        html.H3(children="Sqft"),
        dcc.RangeSlider(
            count=1, min=min_sqft, max=max_sqft, step=1, value=[min_sqft, max_sqft]
        ),
    ]
)

zip_codes = [{"label": x, "value": x} for x in data["zipcode"].sort_values().unique()]
zip_code = html.Div(
    [html.H3(children="Zip Code"), dcc.Dropdown(options=zip_codes, multi=True)]
)

layout = html.Div(
    [
        nav("/building-energy-models"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.P(
                                    children="""
                
                    Explore the accuracy of building energy simulations.

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
                                        year_built_selector,
                                        # building_type_selector,
                                        number_of_stories_selector,
                                        sqft_selector,
                                        zip_code,
                                    ],
                                    className="u-cf",
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
                                    [
                                        dcc.Slider(
                                            min=1, max=20, value=5, id="bem-accuracy-slider"
                                        )
                                    ],
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
                                                    id="bem-savings-accuracy",
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
                                            children=[
                                                html.A("More →", id="more-accuracy")
                                            ],
                                            className="help",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        dcc.Graph(
                                                            id="accuracy-graph",
                                                            config={
                                                                "displayModeBar": False
                                                            },
                                                        )
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.P(
                                            children=[
                                                html.Span(
                                                    "Privacy Cost:",
                                                    className="fancyLabel",
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
                                            id="bem-submit",
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
                                        html.H3("845", id="bem-total-projects"),
                                        html.P("Total Projects"),
                                    ],
                                    className="numberEmphasisChart",
                                ),
                                html.Div(
                                    [
                                        html.H3("-", id="bem-average-savings"),
                                        html.P("Energy Use Intensity (EUI)"),
                                        html.P("at 95% confidence", className="help"),
                                    ],
                                    className="numberEmphasisChart",
                                ),
                                html.Div(
                                    [
                                        html.H3("-", id="cvrmse"),
                                        html.P("CVRMSE"),
                                        html.P("at 95% confidence", className="help"),
                                    ],
                                    className="numberEmphasisChart",
                                ),
                                html.Div(
                                    [
                                        html.H3("-", id="nmbe"),
                                        html.P("NMBE"),
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
                            id="bem-map",
                            style={"height": "100vh"},
                        )
                    ],
                    className="six columns",
                    style={"margin-left": "0", "width": "50%"},
                ),
            ]
        ),
        html.Div(id="bem-past-clicks", style={"display": "none"}),
    ],
    className="",
)
