import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(
    page_title="Fantastic Trains and where to find them",
    layout="wide",
    initial_sidebar_state="expanded"
)




# Load data
heatmap_df2 = pd.read_csv("data/heatmap.csv")
df_states = pd.read_csv("data/statedelay.csv")
df = pd.read_csv("data/fromAPI/cleaned_hourly_all2.csv")

# States processing
df_state_count_delay3 = df[df["departure_delay_check"] == "delay"].groupby(["state"], as_index=False).count()
df_state_count3 = df.groupby(["state"], as_index=False).count()
df_state_sum3 = df[df["departure_delay_check"] == "delay"].groupby(["state"], as_index=False).sum("departure_delay_m")

# Merging state data
df_state = pd.merge(df_state_sum3, df_state_count3[["state", "departure_plan"]], how='left', on="state", suffixes=('', '_count'))
df_state = pd.merge(df_state, df_state_count_delay3[["state", "departure_delay_check"]], how='left', on="state", suffixes=('', '_count'))

df_state["delay_m/departure"] = df_state["departure_delay_m"] / df_state["departure_plan"]
df_state["delay_m/delay_cnt"] = df_state["departure_delay_m"] / df_state["departure_delay_check"]
df_state["delay_cnt/departure"] = (df_state["departure_delay_check"] / df_state["departure_plan"]) * 100

# Cities processing
df_city_count_delay3 = df[df["departure_delay_check"] == "delay"].groupby(["name", "state"], as_index=False).count()
df_city_count3 = df.groupby(["name", "state"], as_index=False).count()
df_city_sum3 = df[df["departure_delay_check"] == "delay"].groupby(["name", "state"], as_index=False).sum("departure_delay_m")

# Merging city data
df_city = pd.merge(df_city_sum3, df_city_count3[["name", "state", "departure_plan"]], how='left', on=["name", "state"], suffixes=('', '_count'))
df_city = pd.merge(df_city, df_city_count_delay3[["name", "state", "departure_delay_check"]], how='left', on=["name", "state"], suffixes=('', '_count'))

df_city["delay_m/departure"] = df_city["departure_delay_m"] / df_city["departure_plan"]
df_city["delay_m/delay_cnt"] = df_city["departure_delay_m"] / df_city["departure_delay_check"]
df_city["delay_cnt/departure"] = (df_city["departure_delay_check"] / df_city["departure_plan"]) * 100





# Sidebar filters
with st.sidebar:
    st.title("DB Delay Dashboard")
    st.sidebar.header("Filters")

    column_selection = st.sidebar.selectbox("Select Measure", options=["departure_plan", "departure_delay_check", "delay_cnt/departure"])

    all_states_option = "All"
    states = st.sidebar.multiselect("State", [all_states_option] + list(df_state['state'].unique()), default=all_states_option)

# Filter data based on selections
if all_states_option in states:
    filtered_data = df_state.copy()  # Select all states, so no filtering needed
else:
    filtered_data = df_state[df_state['state'].isin(states)]

# Display city-level data if only one state is selected
if len(states) == 1 and all_states_option not in states:
    selected_state = states[0]
    state_filtered_data = df_city[df_city['state'] == selected_state]

    # 1st graph for cities within the selected state
    fig0 = px.bar(
        state_filtered_data.sort_values(by=column_selection, ascending=False).head(16),
        y="name", 
        x=column_selection,
        color="name",
        title=f"Top 16 Cities in {selected_state} by {column_selection.replace('_', ' ').capitalize()}",
        height=350,
    )

    # 2nd graph for cities within the selected state
    fig1 = px.bar(
        state_filtered_data.sort_values(by="departure_plan", ascending=False).head(16),
        y="name", 
        x="delay_cnt/departure",
        color="name",
        title=f"Top 16 Cities in {selected_state} by delays/departure %",
        height=350,
    )
else:
    # 1st graph
    fig0 = px.bar(
        filtered_data.sort_values(by=column_selection, ascending=False).head(16),
        y="state", 
        x=column_selection,
        color="state",
        title=f"Top 16 States by {column_selection.replace('_', ' ').capitalize()}",
        height=350,
    )

    # 2nd graph
    fig1 = px.bar(
        filtered_data.sort_values(by="delay_cnt/departure", ascending=False).head(16),
        y="state", 
        x="delay_cnt/departure",
        color="state",
        title=f"Top 16 States by delays/departure %",
        height=350,
    )

col0, col1 = st.columns(2)

with col0:
    st.plotly_chart(fig0)
with col1:
    st.plotly_chart(fig1)

col2, col3 = st.columns(2)

if len(states) == 1 and all_states_option not in states:
    # 3rd graph for cities within the selected state
    fig2 = px.bar(
        state_filtered_data.sort_values(by="departure_plan", ascending=False).head(16),
        y="name", 
        x="delay_m/departure",
        color="name",
        title=f"Top 16 Cities in {selected_state} by delay_m/departure",
        height=350,
    )

    # 4th graph for cities within the selected state
    fig3 = px.bar(
        state_filtered_data.sort_values(by="departure_plan", ascending=False).head(16),
        y="name", 
        x="departure_plan",
        color="name",
        title=f"Top 16 Cities in {selected_state} by departures",
        height=350,
    )
else:
    # 3rd graph
    fig2 = px.bar(
        filtered_data.sort_values(by="delay_cnt/departure", ascending=False).head(16),
        y="state", 
        x="delay_m/departure",
        color="state",
        title=f"Top 16 States by delay_m/departure",
        height=350,
    )

    # 4th graph
    fig3 = px.bar(
        filtered_data.sort_values(by="delay_cnt/departure", ascending=False).head(16),
        y="state", 
        x="departure_plan",
        color="state",
        title=f"Top 16 States by departures",
        height=350,
    )

with col2:
    st.plotly_chart(fig2)
with col3:
    st.plotly_chart(fig3)
