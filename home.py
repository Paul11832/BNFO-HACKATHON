from dash import html, dcc
from navbar import create_navbar
import plotly.express as px

nav = create_navbar()

header = html.H2('RamPantry Map', style={'text-align': 'center', 'padding': '16px'})

df = px.data.gapminder().query("year==2007")
fig = px.scatter_geo(df, locations="iso_alpha", color="continent",
                     hover_name="country", size="pop",
                     projection="natural earth")

def create_page_home():
    layout = html.Div([
        nav,
        header,
        dcc.Graph(figure=fig)
    ])
    return layout
