import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st



st.title("Fantastic Trains and where to find them")

df = pd.read_csv("data/states.csv")
heatmap_df2 = pd.read_csv("data/heatmap.csv")

st.write(df)

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
    color_continuous_scale="Viridis"
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
    color_continuous_scale="Viridis"
)

fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},  # Reduced margins
    coloraxis_showscale=False
    )

st.plotly_chart(fig2)