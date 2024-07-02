from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data/fromAPI/cleaned_hourly_all.csv")

# Creating time and date features
date_format = "%Y-%m-%d %H:%M:%S"
df["arrival_plan"] = pd.to_datetime(df["arrival_plan"], format=date_format)
df["departure_plan"] = pd.to_datetime(df["departure_plan"], format=date_format)
df["arrival_change"] = pd.to_datetime(df["arrival_change"], format=date_format)
df["departure_change"] = pd.to_datetime(df["departure_change"], format=date_format)

df["arrival_plan_time"] = df["arrival_plan"].dt.time
df["arrival_plan_date"] = df["arrival_plan"].dt.date

# Drop DB defined trains which have no delay up to 6 minutes
df.drop(df[df["arrival_delay_m"] < 6].index, inplace=True)

# Creating new columns to convert the datetime delay into 24 unique hours to have a slider on our dashboard
df["Day_delay"] = df["arrival_plan"].dt.date
df["Hour_delay"] = df["arrival_plan"].dt.hour

# Combine Day and Hour into a single string for animation_frame
df["DayHour"] = df["Day_delay"].astype(str) + ' ' + df["Hour_delay"].astype(str) + ':00'

# Filter out the data where arrival_delay_check is not "on_time"
#filtered_df = df[df["arrival_delay_check"] != "on_time"]

# Group by necessary columns
grouped_df = df.groupby(["DayHour", "name", "long", "lat", "category"], as_index=False).mean(numeric_only=True)

# Create the figure with animation
fig = px.scatter_mapbox(
    grouped_df,
    title="Train Delays Over Time",
    lon='long', lat='lat',
    hover_name='name',
    size="arrival_delay_m",
    color="category",
    size_max=20,
    zoom=10,
    animation_frame="DayHour",
    color_continuous_scale=px.colors.sequential.Inferno
)

# Update layout and setting the map
fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_center={"lat": 51.1657, "lon": 10.4515},  # Centered on Germany
    mapbox_zoom=5,
    width=700,
    height=800
)

# Initialize the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Train delay'),

    html.Div(children='''
        A dashboard to showcase the distribution of train delay.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
