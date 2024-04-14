import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')

# Create a bubble map
fig = px.scatter_mapbox(df, lat="lat", lon="long", size="cnt", color="cnt",
                        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15,
                        center=dict(lat=37.5485, lon=-77.4527), zoom=16, # Center on Virginia Commonwealth University
                        mapbox_style="carto-positron")

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig, style={'height': '800px'})  # Set the height to 800px
])

if __name__ == '__main__':
    app.run_server(debug=True)