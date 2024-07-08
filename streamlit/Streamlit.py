import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st



st.title("Fantastic Trains and where to find them")

df = pd.read_csv("data/fromAPI/cleaned_hourly_all2.csv")
st.write(df)
