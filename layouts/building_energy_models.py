# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from .nav import nav

from db import building_energy_models_data as data

outputs = {
    "eui": {"label": "Energy Use Intensity (EUI)", "value_range": 2000},
    "cvrmse": {"label": "CVRMSE", "value_range": 10},
    "nmbe": {"label": "NMBE", "value_range": 50},
}

output_options = [{"label": o["label"], "value": k} for k, o in outputs.items()]

output_selector = html.Div(
    [dcc.Dropdown(options=output_options, value="eui", id="bem-output-choice")]
)


max_year_built = data["year_built"].max()
min_year_built = data["year_built"].min()
year_built_selector = html.Div(
    [
        html.H3(children="Year Built"),
        html.Div(
            [
                dcc.RangeSlider(
                    id="bem-year-built",
                    count=1,
                    min=min_year_built,
                    max=max_year_built,
                    step=1,
                    value=[min_year_built, max_year_built],
                    tooltip={"always_visible": True, "placement": "bottom"},
                )
            ],
            style={"padding": "0 20px 40px 20px"},
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
    [
        html.H3(children="Number of Stories"),
        dcc.Dropdown(id="bem-number-of-stories", options=floors, multi=True),
    ]
)

min_sqft = data["sqft"].min()
max_sqft = data["sqft"].max()
sqft_selector = html.Div(
    [
        html.H3(children="Sqft"),
        html.Div(
            [
                dcc.RangeSlider(
                    id="bem-sqft",
                    count=1,
                    min=min_sqft,
                    max=max_sqft,
                    step=1,
                    value=[min_sqft, max_sqft],
                    tooltip={"always_visible": True, "placement": "bottom"},
                )
            ],
            style={"padding": "0 20px 40px 20px"},
        ),
    ]
)

zip_codes = [{"label": x, "value": x} for x in data["zipcode"].sort_values().unique()]
zip_code = html.Div(
    [
        html.H3(children="Zip Code"),
        dcc.Dropdown(id="bem-zipcode", options=zip_codes, multi=True),
    ]
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
                                    ]
                                ),
                                html.H2("Output", style={"marginTop": "40px"}),
                                html.Div([output_selector]),
                                html.H2("Accuracy", style={"marginTop": "40px"}),
                                html.P(""),
                                html.Div(
                                    [
                                        dcc.Slider(
                                            min=1,
                                            max=20,
                                            value=5,
                                            id="bem-accuracy-slider",
                                        )
                                    ],
                                    style={"padding": "15px 0 0 0"},
                                ),
                                html.Div(
                                    [
                                        html.P(
                                            children=[
                                                html.Span(
                                                    "Average Accuracy:",
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
                                                "95% confidence interval for average result. Smaller is better."
                                            ],
                                            className="help",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        dcc.Graph(
                                                            id="bem-accuracy-graph"
                                                        )
                                                    ],
                                                    id="bem-accuracy-graph-container",
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
                                        html.H3("-", id="bem-output"),
                                        html.P(
                                            "Energy Use Intensity (EUI)",
                                            id="bem-output-label",
                                        ),
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
                    className="six columns leftContainer",
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
                    style={"marginLeft": "0", "width": "50%"},
                ),
            ]
        ),
        html.Div(id="bem-past-clicks", style={"display": "none"}),
    ],
    className="",
)
