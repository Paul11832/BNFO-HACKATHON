from dash import html, dcc
from navbar import create_navbar
import plotly.express as px
import pandas as pd

data = pd.read_excel("formatted_info.xlsx")

data["Month"] = data["Date"].dt.month

# Group by location, latitude, longitude, and month, and count the occurrences
grouped_data = (
    data.groupby(["Location", "Latitude", "Longitude", "Month"])
    .size()
    .reset_index(name="Occurrences")
)

# Rename columns to match the user's request
grouped_data.rename(
    columns={"Latitude": "lat", "Longitude": "lon", "Location": "location"},
    inplace=True,
)

# Reorder columns as specified
final_data = grouped_data[["lat", "lon", "location", "Occurrences", "Month"]]

final_data.to_excel("final_data.xlsx", index=False)

nav = create_navbar()

header = html.H2("RamPantry Map", style={"text-align": "center", "padding": "16px"})

fig = px.scatter_mapbox(
    final_data,
    lat="lat",
    lon="lon",
    color="location",
    size="Occurrences",
    zoom=16,
    center={"lat": 37.544100, "lon": -77.438670},
    height=600,
    size_max=30,
)
fig.update_layout(mapbox_style="open-street-map")

def get_final_data():
    return final_data

def create_page_home():
    layout = html.Div(
        [
            nav,
            header,
            dcc.Graph(id="map_shit", figure=fig),
            dcc.Slider(
                min=1,
                max=12,
                step=1,
                value=1,
                marks={i: str(i) for i in range(1, 13)},
                id="month-slider"
            ),
        ]
    )
    return layout
