import dash_html_components as html

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
