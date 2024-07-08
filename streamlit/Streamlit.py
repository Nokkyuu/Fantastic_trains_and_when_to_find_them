
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
df_station = pd.read_csv("data/stations.csv")


#Barcharts states 
fig0, axes = plt.subplots(1, 4, figsize=(12, 4), constrained_layout=True)

sns.barplot(data=df_station.sort_values(by="departure_plan", ascending=False).head(15), y="name", x="departure_plan", 
            palette="flare", orient="h", hue="departure_plan", ax=axes[0])
axes[0].set_xlabel(f"departures")
axes[0].tick_params(axis='x', rotation=90)
axes[0].set_ylabel("")
axes[0].get_legend().remove()

    

sns.barplot(data=df_station.sort_values(by="departure_plan", ascending=False).head(15), y="name", x="delay_cnt/departure", 
            palette="flare", orient="h", hue="departure_plan", ax=axes[1])
axes[1].set_xlabel(f"delays/departure %")
axes[1].tick_params(axis='x', rotation=90)
axes[1].get_legend().remove()
axes[1].get_yaxis().set_visible(False)


sns.set_theme(style="whitegrid")
sns.barplot(data=df_station.sort_values(by="departure_plan", ascending=False).head(15), y="name", x="delay_m/departure", 
            palette="flare", orient="h", hue="departure_plan", ax=axes[2])
axes[2].set_xlabel(f"delay_m/departure")
axes[2].tick_params(axis='x', rotation=90)
axes[2].get_legend().remove()
axes[2].get_yaxis().set_visible(False)

sns.barplot(data=df_station.sort_values(by="departure_plan", ascending=False).head(15), y="name", x="delay_m/delay_cnt", 
            palette="flare", orient="h", hue="departure_plan", ax=axes[3])
axes[3].set_xlabel(f"avg_minutes/delay")
axes[3].tick_params(axis='x', rotation=90)
#axes[3].get_legend().remove()
axes[3].get_yaxis().set_visible(False)
axes[3].legend(title="departure Plan")

st.plotly_chart(fig0)





#add sidebar for filters
st.sidebar.header("Filters")
states = st.sidebar.multiselect("State", df['state'].unique())

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