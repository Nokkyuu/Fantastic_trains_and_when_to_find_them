import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, time, datetime
from IPython import display
import os



# Page config
st.set_page_config(
    page_title="Fantastic Trains and where to find them",
    layout="wide",
    initial_sidebar_state="expanded"
)




# Load data
heatmap_df2 = pd.read_csv("data/heatmap.csv")
df_states = pd.read_csv("data/statedelay.csv")
df = pd.read_csv("data/fromAPI/streamlit.csv")

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
df_city_count_delay3 = df[df["departure_delay_check"] == "delay"].groupby(["station", "state"], as_index=False).count()
df_city_count3 = df.groupby(["station", "state"], as_index=False).count()
df_city_sum3 = df[df["departure_delay_check"] == "delay"].groupby(["station", "state"], as_index=False).sum("departure_delay_m")

# Merging city data
df_city = pd.merge(df_city_sum3, df_city_count3[["station", "state", "departure_plan"]], how='left', on=["station", "state"], suffixes=('', '_count'))
df_city = pd.merge(df_city, df_city_count_delay3[["station", "state", "departure_delay_check"]], how='left', on=["station", "state"], suffixes=('', '_count'))

df_city["delay_m/departure"] = df_city["departure_delay_m"] / df_city["departure_plan"]
df_city["delay_m/delay_cnt"] = df_city["departure_delay_m"] / df_city["departure_delay_check"]
df_city["delay_cnt/departure"] = (df_city["departure_delay_check"] / df_city["departure_plan"]) * 100





#datetime
df2 = df.copy()

date_format = "%Y-%m-%d %H:%M:%S"
df2["arrival_plan"] = pd.to_datetime(df2["arrival_plan"], format=date_format)
df2["departure_plan"] = pd.to_datetime(df2["departure_plan"], format=date_format)
df2["arrival_change"] = pd.to_datetime(df2["arrival_change"], format=date_format)
df2["departure_change"] = pd.to_datetime(df2["departure_change"], format=date_format)

df2["arrival_plan_time"] = df2["arrival_plan"].dt.time
df2["arrival_plan_date"] = df2["arrival_plan"].dt.date

df2["departure_plan_time"] = df2["departure_plan"].dt.time
df2["departure_plan_date"] = df2["departure_plan"].dt.date





#Logo
ICON_RED = "https://preview.redd.it/deutsche-bahn-logo-bauen-r-place-v0-60xms5wt0ddb1.png?width=814&format=png&auto=webp&s=c634c8b94115358ab48c2913ef349afe63d4671d"
st.logo(ICON_RED, icon_image=ICON_RED)



#Button to our Github
col_head, col_pic = st.columns([5, 1])
with col_head:
    st.link_button("Github :sunglasses:", "https://github.com/Nokkyuu/Fantastic_trains_and_where_to_find_them")
    st.subheader("DB Delay Dashboard")
with col_pic:
    st.image("streamlit/deutsche-bahn-logo-bauen-r-place-v0-60xms5wt0ddb1.png", use_column_width="auto")

# Sidebar filters
with st.sidebar:
    st.sidebar.header("Filters")

    all_states_option = "All"
    states = st.sidebar.selectbox("Select State", [all_states_option] + list(df_state['state'].unique()), index=0)

    column_selection = st.sidebar.selectbox("Sort By (Geo)", options=["departure_plan", "delay_cnt/departure", "delay_m/delay_cnt", "delay_m/departure"])

   





#making tabs
tab0, tab1, tab2 = st.tabs(["Introduction","Temporal", "Geographical"])




with tab0:
    # Filter data based on selections
    if states == all_states_option:
        filtered_df = df.copy()  # Select all data
    else:
        filtered_df = df[df['state'] == states]  # Filter data based on selected state

    # Summary metrics
    if states == all_states_option:
        st.markdown("### Summary Metrics for All States")
    else:
        st.markdown(f"### Summary Metrics for {states}")


    #defining metrics
    average_delay = filtered_df['departure_delay_m'].mean()
    num_delayed_departures = filtered_df[filtered_df['departure_delay_m'] > 0]['departure_delay_m'].count() 

    total_departures = filtered_df['departure_plan'].count() 
    total_delay_minutes = filtered_df['arrival_delay_m'].sum() + filtered_df['departure_delay_m'].sum() 
    num_delayed_arrivals = filtered_df[filtered_df['arrival_delay_m'] > 0]['arrival_delay_m'].count() 

    total_delays = num_delayed_arrivals + num_delayed_departures

    # First row of metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric(label="Total Number of Departures", value=total_departures * 5)
    with metric_col2:
        st.metric(label="Total Delay in Minutes", value=f"{total_delay_minutes * 5} min")
    with metric_col3:
        st.metric(label="Number of Delayed Departures", value=num_delayed_departures * 5)

    # Second row of metrics
    metric_col4, metric_col5, metric_col6 = st.columns(3)
    with metric_col4:
        st.metric(label="Total Delays", value=total_delays * 5)
    with metric_col5:
        st.metric(label="Average Delay Time", value=f"{average_delay:.2f} min")
    with metric_col6:
        st.metric(label="Number of Delayed Arrivals", value=num_delayed_arrivals * 5)




    # Section for data source and additional information
    st.markdown("---")
    st.markdown("### Data Source and Additional Information")

    st.markdown(
        """
        **Data Source**: The data for this dashboard is sourced from multiple datasets gathered via API from Deutsche Bahn.

        **Processing**: Data was processed and cleaned to ensure accuracy and consistency. For detailed information please refer to our [GitHub repository](https://github.com/Nokkyuu/Fantastic_trains_and_where_to_find_them).

        **Acknowledgments**: We would like to thank Deutsche Bahn and the open data community for providing the data and making this dashboard possible.
        """
    )

    st.markdown(
        """
        **Developed by**: Michael Kampmann, Nils Ayral

        **Version**: 1.0

        **Last Updated**: July 2024
        """
    )






with tab1:
    st.subheader("Departure Delays over Time")
    fig6 = px.density_mapbox(
        heatmap_df2,
        lat='lat',
        lon='long',
        z='departure_delay_m',
        hover_name="station",
        radius=15,
        range_color=[0, heatmap_df2.departure_delay_m.max()],
        mapbox_style="carto-positron",
        center={"lat": 51.1657, "lon": 10.4515},
        zoom=4.5,
        animation_frame="departure_plan_datetime",
        color_continuous_scale=px.colors.sequential.Inferno,
        height=600
    )
    fig6.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        coloraxis_showscale=False
    )
    st.plotly_chart(fig6)    


    st.markdown("---")


    # Function to plot datetime
    st.subheader("Mean Delay over Time")
    st.text("Search for periodic patterns")
    def plot_data(df_temp, state):
        fig, axes = plt.subplots(1, 1, figsize=(12, 4), constrained_layout=True)
        df_temp.set_index('departure_plan', inplace=True)
        numeric_cols = df_temp.select_dtypes(include=['float64', 'int64'])
        hourly_data = numeric_cols.resample('h').mean()

        sns.lineplot(data=hourly_data, x=hourly_data.index, y="departure_delay_m", ax=axes)
        axes.set_xlabel("")
        axes.set_ylabel("Delay Mean")
        axes.tick_params(axis='x', rotation=90)

        fig.suptitle(state, fontsize=16)
        st.pyplot(fig)

    # Plotting the data based on selection
    if states == all_states_option:
        # Plot for all states
        df_temp = df2.copy()  # Use the original dataframe for all states
        plot_data(df_temp, "All States")
    else:
        # Plot for the selected state
        df_temp = df2[df2['state'] == states]  # Filter the dataframe for the selected state
        plot_data(df_temp, states)

    st.markdown("---")


    st.subheader("25% best and 25% worst stations hourly observation Germany")
    st.image("streamlit/bestworststat.png")



# Tab2

with tab2:
    # Filter data based on selections
    if states == all_states_option:
        filtered_data = df_state.copy()  # Select all states, so no filtering needed
    else:
        filtered_data = df_state[df_state['state'] == states]

    # Display city-level data if only one state is selected
    if states != all_states_option:
        selected_state = states
        state_filtered_data = df_city[df_city['state'] == selected_state]

        # 1st graph for cities within the selected state
        fig0 = px.bar(
            state_filtered_data.sort_values(by=column_selection, ascending=False).head(16),
            y="station", 
            x="departure_plan",
            color="station",
            title=f"Number of Departure Events",
            height=450,
            labels={"departure_plan" : "# of departures planned", "station" : "station"}
        )
        #fig0.update(layout_showlegend=False)
        # 2nd graph for cities within the selected state
        fig1 = px.bar(
            state_filtered_data.sort_values(by=column_selection, ascending=False).head(16),
            y="station", 
            x="delay_cnt/departure",
            color="station",
            title=f"% of delays per departure",
            height=450,
            labels={"delay_cnt/departure" : "% of delays from departures", "station" : "station"}
        )
        #fig1.update(layout_showlegend=False)
        fig2 = px.bar(
            state_filtered_data.sort_values(by=column_selection, ascending=False).head(16),
            y="station", 
            x="delay_m/delay_cnt",
            color="station",
            title=f"Average Delay Length per Delay",
            height=450,
            labels={"delay_m/delay_cnt" : "Avg. delay length (m)", "station" : "station"}
        )
        fig3 = px.bar(
            state_filtered_data.sort_values(by=column_selection, ascending=False).head(16),
            y="station", 
            x="delay_m/departure",
            color="station",
            title=f"Average Delay Length per Departure",
            height=450,
            labels={"delay_m/departure" : "Length of Delay/Departure (m)"}
        )

    else:
        fig0 = px.bar(
            filtered_data.sort_values(by=column_selection, ascending=False).head(16),
            y="state", 
            x="departure_plan",
            color="state",
            title=f"Number of Departure Events",
            height=450,
            labels={"departure_plan" : "# of departures planned"}
        )
        # 2nd graph for cities within the selected state
        fig1 = px.bar(
            filtered_data.sort_values(by=column_selection, ascending=False).head(16),
            y="state", 
            x="delay_cnt/departure",
            color="state",
            title=f"% of delays from departures",
            height=450,
            labels={"delay_cnt/departure" : "% of delays from departures"}
        )
        fig2 = px.bar(
            filtered_data.sort_values(by=column_selection, ascending=False).head(16),
            y="state", 
            x="delay_m/delay_cnt",
            color="state",
            title=f"Average Delay Length per Delay",
            height=450,
            labels={"delay_m/delay_cnt" : "Length of Delay/Delay (m)"}
        )
        fig3 = px.bar(
            filtered_data.sort_values(by=column_selection, ascending=False).head(16),
            y="state", 
            x="delay_m/departure",
            color="state",
            title=f"Average Delay Length per Departure",
            height=450,
            labels={"delay_m/departure" : "Length of Delay/Departure (m)"}
        )
    fig1.update_yaxes(visible=False, showticklabels=False)
    fig2.update_yaxes(visible=False, showticklabels=False)
    fig3.update_yaxes(visible=False, showticklabels=False)
    fig0.update(layout_showlegend=False)
    fig1.update(layout_showlegend=False)
    fig2.update(layout_showlegend=False)
    fig3.update(layout_showlegend=False)
    col0, col1, col2, col3 = st.columns(4)

    with col0:
        st.plotly_chart(fig0)
    with col1:
        st.plotly_chart(fig1)
    with col2:
        st.plotly_chart(fig2)
    with col3:
        st.plotly_chart(fig3)

    # {col2, col3 = st.columns(2)

    # if states != all_states_option:
    #     # 3rd graph for cities within the selected state
    #     fig2 = px.bar(
    #         state_filtered_data.sort_values(by=column_selection, ascending=False).head(16),
    #         y="station", 
    #         x="delay_m/departure",
    #         color="station",
    #         title=f"Top 16 Stations in {selected_state} by delay_m/departure",
    #         height=350,
    #     )

    #     # 4th graph for cities within the selected state
    #     fig3 = px.bar(
    #         state_filtered_data.sort_values(by=column_selection, ascending=False).head(16),
    #         y="station", 
    #         x="delay_m/delay_cnt",
    #         color="station",
    #         title=f"Top 16 Stations in {selected_state} by departures",
    #         height=350,
    #     )
    # else:
    #     # 3rd graph
    #     fig2 = px.bar(
    #         filtered_data.sort_values(by=column_selection, ascending=False).head(16),
    #         y="state", 
    #         x="delay_m/delay_cnt",
    #         color="state",
    #         title=f"Top 16 States by delay_m/delay_cnt",
    #         height=350,
    #     )

    #     # 4th graph
    #     fig3 = px.bar(
    #         filtered_data.sort_values(by=column_selection, ascending=False).head(16),
    #         y="state", 
    #         x="departure_plan",
    #         color="state",
    #         title=f"Top 16 States by departures",
    #         height=350,
    #     )

    # with col2:
    #     st.plotly_chart(fig2)
    # with col3:
    #     st.plotly_chart(fig3)}


    st.markdown("---")

    
    # Heatmap with mean delays
    st.subheader("Heatmap for departure delays (mean)")
    fig5 = px.density_mapbox(
        heatmap_df2,
        lat='lat',
        lon='long',
        z='departure_delay_m',
        hover_name="station",
        radius=7,
        range_color=[0, heatmap_df2.departure_delay_m.max()],
        mapbox_style="carto-positron",
        center={"lat": 51.1657, "lon": 10.4515},
        zoom=4.5,
        color_continuous_scale="Magma",
        height=456
    )
    fig5.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        coloraxis_showscale=True,
    )
    st.plotly_chart(fig5)




 
  

