import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Title
st.title("Fantastic Trains and Where to Find Them")

# Load data
df = pd.read_csv("data/states.csv")
heatmap_df2 = pd.read_csv("data/heatmap.csv")
df_station = pd.read_csv("data/statedelay.csv")

# Sidebar filters
st.sidebar.header("Filters")

column_selection = st.sidebar.selectbox("Select Measure", options=["departure_delay_m", "departure_plan", "departure_delay_check", "delay_m/departure", "delay_m/delay_cnt", "delay_cnt/departure"])

all_states_option = "All"
states = st.sidebar.multiselect("State", [all_states_option] + list(df_station['state'].unique()), default=all_states_option)



# Filter data based on selections
if all_states_option in states:
    filtered_data = df_station.copy()  # Select all states, so no filtering needed
else:
    filtered_data = df_station[df_station['state'].isin(states)]

# Barchart of delays per state
st.subheader("State Delays")
fig0 = px.bar(
    filtered_data.sort_values(by=column_selection, ascending=False).head(16),
    y="state", 
    x=column_selection,
    color="state",
    title=f"Top 16 States by {column_selection.replace('_', ' ').capitalize()}",
    color_continuous_scale="Magma"
)
st.plotly_chart(fig0)

# Heatmap with timeseries
st.subheader("Map of Germany - Departure Delays Over Time")
fig1 = px.density_mapbox(
    heatmap_df2,
    lat='lat',
    lon='long',
    z='departure_delay_m',
    hover_name='name',
    radius=10,
    range_color=[0, heatmap_df2.departure_delay_m.max()],
    mapbox_style="carto-positron",
    center={"lat": 51.1657, "lon": 10.4515},
    zoom=4.5,
    title="Departure Delays Over Time",
    animation_frame="departure_plan_datetime",
    color_continuous_scale="Magma",
    height=600
)
fig1.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    coloraxis_showscale=False
)
st.plotly_chart(fig1)

# Heatmap with mean delays
st.subheader("Map of Germany - Departure Delays Heatmap")
fig2 = px.density_mapbox(
    heatmap_df2,
    lat='lat',
    lon='long',
    z='departure_delay_m',
    hover_name='name',
    radius=10,
    range_color=[0, heatmap_df2.departure_delay_m.max()],
    mapbox_style="carto-positron",
    center={"lat": 51.1657, "lon": 10.4515},
    zoom=4.5,
    title="Departure Delays Heatmap",
    color_continuous_scale="Magma",
    height=600
)
fig2.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    coloraxis_showscale=False
)
st.plotly_chart(fig2)

# Add more sections or interactivity as needed
