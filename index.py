from dash import html, dcc
from dash.dependencies import Input, Output
from home import create_page_home
from page_2 import create_page_2
from page_3 import create_page_3
import plotly.express as px
import pandas as pd
from app import app
from home import get_final_data

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

df = pd.read_excel("formatted_info.xlsx")

# Combine date and time into a single datetime column
df["Datetime"] = pd.to_datetime(df["Date"]) + pd.to_timedelta(df["Time"])

# Sort the dataframe by the new datetime column
df.sort_values("Datetime", inplace=True)

# Assume 'Datetime' column is already converted to datetime dtype
# If 'Datetime' column is not found, adjust the column name in the code below

# Aggregate data by hour, month, and year
df["Hour"] = df["Datetime"].dt.hour
df["Month"] = df["Datetime"].dt.month
df["Year"] = df["Datetime"].dt.year

# You might also want full date without time for daily aggregation
df["Date"] = df["Datetime"].dt.date

# Extracting the weekday from the Datetime column
df["Weekday"] = df["Datetime"].dt.day_name()  # This will give you the name of the day

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/page-2":
        return create_page_2()
    if pathname == "/page-3":
        return create_page_3()
    else:
        return create_page_home()


@app.callback(
    Output("time-series-chart", "figure"), Input("time-interval-dropdown", "value")
)
def update_graph(selected_interval):
    if selected_interval == "Hour":
        df_group = df.groupby(df["Datetime"].dt.hour).size().reset_index(name="Counts")
        df_group.rename(columns={"Datetime": "Hour"}, inplace=True)
        fig = px.line(df_group, x="Hour", y="Counts", title="Hourly Events")
    elif selected_interval == "Day":
        df_group = df.groupby(df["Datetime"].dt.date).size().reset_index(name="Counts")
        df_group.rename(columns={"Datetime": "Date"}, inplace=True)
        fig = px.line(df_group, x="Date", y="Counts", title="Daily Events")
    elif selected_interval == "Weekday":
        fig = px.histogram(df, x="Weekday", title="Histogram of Weekdays")
    elif selected_interval == "Month":
        df_group = (
            df.groupby(df["Datetime"].dt.to_period("M"))
            .size()
            .reset_index(name="Counts")
        )
        df_group["Month"] = df_group["Datetime"].dt.to_timestamp()
        fig = px.line(df_group, x="Month", y="Counts", title="Monthly Events")
    elif selected_interval == "Year":
        df_group = df.groupby(df["Datetime"].dt.year).size().reset_index(name="Counts")
        df_group.rename(columns={"Datetime": "Year"}, inplace=True)
        fig = px.line(df_group, x="Year", y="Counts", title="Yearly Events")

    return fig

@app.callback(
    Output('map_shit', 'figure'),
    [Input('month-slider', 'value')]
)
def update_figure(selected_month):
    final_data = get_final_data()
    filtered_data = final_data[final_data['Month'] == selected_month]

    fig = px.scatter_mapbox(
        filtered_data,
        lat="lat",
        lon="lon",
        color="location",
        size="Occurrences",
        zoom=16,
        center={"lat": 37.5483, "lon": -77.4527},
        height=600,
        size_max=30,
    )
    fig.update_layout(mapbox_style="open-street-map")

    return fig

if __name__ == "__main__":
    app.run(debug=True)
