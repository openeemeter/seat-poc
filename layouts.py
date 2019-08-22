# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

def nav(active):
    def nav_classes(pathName):
        if active == pathName:
            return "active"
        else:
            return ""

    return html.Div(
        className="nav",
        children=[
            html.H3(children="SEAT", className="brand"),
            html.A("Efficiency Impact Explorer", href="/", className=nav_classes("/")),
            html.A(
                "Model Calibration and Verification",
                href="/building-energy-models",
                className=nav_classes("/building-energy-models"),
            ),
        ],
    )


app_layout = html.Div(
    [
        nav("/"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2(
                                    children=[
                                        html.Span(
                                            children="California",
                                            className="locationTitle",
                                        ),
                                        html.Span(children="/"),
                                        html.Span(
                                            children="2018", className="yearTitle"
                                        ),
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
                                                        {
                                                            "label": "Office",
                                                            "value": "Office",
                                                        },
                                                        {
                                                            "label": "Hotel",
                                                            "value": "Hotel",
                                                        },
                                                    ],
                                                    value="All Buildings",
                                                    id="building-type",
                                                ),
                                            ],
                                            className="five columns",
                                        ),
                                        html.Div(
                                            [
                                                html.H3(
                                                    children="Energy Conservation Measure"
                                                ),
                                                dcc.RadioItems(
                                                    options=[
                                                        {
                                                            "label": "All",
                                                            "value": "All ECMS",
                                                        },
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
                                    children=html.Div(
                                        [html.A("Upload Custom Portfolio File")]
                                    ),
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
                                    [
                                        dcc.Slider(
                                            min=1, max=20, value=5, id="accuracy-slider"
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
            ]
        ),
        html.Div(id="past-clicks", style={"display": "none"}),
    ],
    className="",
)
