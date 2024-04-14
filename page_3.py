from dash import dcc, html
from navbar import create_navbar
import plotly.express as px
from home import get_final_data

df = get_final_data()

summed_data = df.groupby(['lat', 'lon', 'location']).agg({'Occurrences': 'sum'}).reset_index()

nav = create_navbar()

header = html.H2("Overall Occurrences", style={"text-align": "center", "padding": "16px"})

shit = px.pie(summed_data, values="Occurrences", names="location", hole=.3, height=600)


def create_page_3():
    layout = html.Div(
        [
            nav,
            header,
            dcc.Graph(figure=shit)
        ]
    )
    return layout
