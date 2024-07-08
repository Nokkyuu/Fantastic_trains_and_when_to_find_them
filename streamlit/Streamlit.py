
import streamlit as st
#Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import date, time, datetime
from IPython import display
import os
import datetime


#title
st.title("Fantastic Trains and where to find them")

#dataframes
df = pd.read_csv("data/states.csv")
heatmap_df2 = pd.read_csv("data/heatmap.csv")
df_station = pd.read_csv("data/statedelay.csv")


#Barcharts states 



sns.set_theme(style="whitegrid")
fig0 = px.bar(df_station.sort_values(by="delay_cnt/departure", ascending=False).head(16),
              y="state", x="delay_m/departure",
                  color_continuous_scale="Magma"
)

st.plotly_chart(fig0)





#add sidebar for filters
st.sidebar.header("Filters")
states = st.sidebar.multiselect("State", df_station['state'].unique())

# Filter data based on selections
if states:
    filtered_data = df_station[df_station['state'].isin(states)]
else:
    filtered_data = df_station



#heatmap with timeseries
st.subheader("Map of Germany")
fig = px.density_mapbox(
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
    width=600,
    height=600,
    title="Departure Delays over time",
    animation_frame="departure_plan_datetime",
    color_continuous_scale="Magma"
)

fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},  # Reduced margins
    coloraxis_showscale=False
    )
st.plotly_chart(fig)

#heatmap with mean
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
    width=600,
    height=600,
    title="Departure Delays Heatmap",
    color_continuous_scale="Magma"
)

fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},  # Reduced margins
    coloraxis_showscale=False
    )

st.plotly_chart(fig2)