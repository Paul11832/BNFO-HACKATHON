from dash import html, dcc
from navbar import create_navbar
import dash_bootstrap_components as dbc


nav = create_navbar()

header = html.H2("Door Event Visualization", style={'text-align': 'center', 'padding': '16px'})

def create_page_2():
    layout = html.Div(
        [
            nav,
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Dropdown(
                                options=[
                                    {"label": "Hourly", "value": "Hour"},
                                    {"label": "Daily", "value": "Day"},
                                    {"label": "Weekday", "value": "Weekday"},
                                    {"label": "Monthly", "value": "Month"},
                                    {"label": "Yearly", "value": "Year"},
                                ],
                                value="Day",
                                id="time-interval-dropdown",
                                style={'margin': '10px'},
                                clearable=False,
                            ),
                        ],
                        md=3,
                        style={'background-color': '#f8f9fa'},
                    ),
                    dbc.Col(
                        [
                            header,
                            dcc.Graph(id="time-series-chart", style={'height': '600px'}),
                        ],
                        md=8,
                    ),
                ]
            ),
        ]
    )
    return layout