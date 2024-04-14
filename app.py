from dash import Dash, dcc, html
import plotly.graph_objects as go
import plotly.express as px

# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# app = Dash(__name__, external_stylesheets=external_stylesheets)

df = px.data.gapminder().query("year==2007")

app = Dash(__name__)

tab1 = dcc.Tab(
    label="Tab one",
    value="tab-1",
    children=[
        px.scatter_geo(df, locations="iso_alpha", color="continent",
                     hover_name="country", size="pop",
                     projection="natural earth")
    ],
)

tab2 = dcc.Tab(
    label="Tab two",
    value="tab-2",
    children=[
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": [1, 2, 3],
                        "y": [1, 4, 1],
                        "type": "bar",
                        "name": "SF",
                    },
                    {
                        "x": [1, 2, 3],
                        "y": [1, 2, 3],
                        "type": "bar",
                        "name": "Montréal",
                    },
                ]
            }
        )
    ],
)

app.layout = html.Div(
    [
        html.Link(rel="stylesheet", href="/static/stylesheet.css"),
        dcc.Tabs(
            id="tabs-styled-with-inline",
            value="tab-1",
            children=[tab1, tab2],
            vertical=True,
        )
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
