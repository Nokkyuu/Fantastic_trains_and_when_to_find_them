import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("data/fromAPI/cleaned_hourly_all.csv")

#creating time and date features
date_format = "%Y-%m-%d %H:%M:%S"
df["arrival_plan"] = pd.to_datetime(df["arrival_plan"], format=date_format)
df["departure_plan"] = pd.to_datetime(df["departure_plan"], format=date_format)
df["arrival_change"] = pd.to_datetime(df["arrival_change"], format=date_format)
df["departure_change"] = pd.to_datetime(df["departure_change"], format=date_format)

df["arrival_plan_time"] = df["arrival_plan"].dt.time
df["arrival_plan_date"] = df["arrival_plan"].dt.date

#drop DB defined trains which have no delay up to 6 minutes
df.drop(df[df["arrival_delay_m"] < 6].index, inplace=True)

#creating a new column to convert the datetime delay into 24 unique hours to have a slider on our dashboard
df["Hour_delay"] = df["departure_plan"].dt.hour
unique_hours = df["Hour_delay"].unique()

#create a dictionary for the slider marks
#marks = {i: time.strftime('%h:%M') for i, time in enumerate(pd.date_range(df['departure_plan'].min(), df['departure_plan'].max(), freq='h'))}
marks = {hour: f"{hour}:00" for hour in range(24)}



# Create a Plotly figure
#fig = px.line(df, x='Date', y='Value', title='Sample Line Chart')

#Plotting the stations with size indicator for the delay -> creating a function
def create_map(hour):
    filtered_df = df[df["Hour_delay"] == hour]
    fig = px.scatter_mapbox(filtered_df, lon='long', lat='lat', hover_name='name', size_max=20, zoom=10,
                            size="arrival_delay_m")

# Update layout and setting the map
    fig.update_layout(mapbox_style="carto-positron",
                  mapbox_center={"lat": 51.1657, "lon": 10.4515},  # Centered on Germany
                  mapbox_zoom=5,
                  width = 700,
                  height = 800)
    return fig


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Train delay'),

    html.Div(children='''
        A dashboard to showcase the distribution of train delay.
    '''),

    #add Slider
    dcc.Slider(
        id='hour-slider',
        min=0,
        max=len(marks) - 1,
        value=0,
        marks=marks,
        step=None
    ),

    dcc.Graph(
        id='example-graph',
    )
])

# Callback function to update the map
@app.callback(
    Output('example-graph', 'figure'),
    [Input('hour-slider', 'value')])

def update_figure(selected_hour):
    return create_map(selected_hour)

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
