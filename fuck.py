#!/usr/bin/env python
# coding: utf-8

# In[89]:


from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

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

# Assume df is already loaded and prepared as per the earlier steps including the 'Weekday' column
app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Door Events Visualization"),
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
        ),
        dcc.Graph(id="time-series-chart"),
    ]
)


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


if __name__ == "__main__":
    app.run_server(debug=True)


# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:
