# Overview

## Data

For detailed description of the features available in the datasets please look into the [data_description.md](data_description.md)

## Folders

1) API:<br> Folder contains scripts for written to handle the different DB APIs
2) Data:
    - fromAPI: contains .csv files created using the DB API
    - so_me: data from social media messages regarding DB from Kaggle
    - train_stops: trainstop data from Kaggle
3) EDA: <br>Contains notebooks regarding the exploratory data analysis part of the different datasets
    - [Comparison regarding the station categories](EDA/01_data_collecting_comparison.ipynb)
    - [Temporal Analysis](EDA/02_temporal_analysis.ipynb)
    - [Geographical Analysis](EDA/03_geographical_analysis.ipynb)<br>
4) ML: <br> Notebooks about the feature creation and Time Series Analysis
    - [Feature Creation](ML/ML_feature_creation_stations_class.ipynb)
    - [Time Series](ML/Time_Series.ipynb)
5) Streamlit: <br> Contains every element for the custom Dashboard
    - [Streamlit Dashboard](streamlit/Streamlit.py)
## Stakeholder
`Deutsche Bahn`


