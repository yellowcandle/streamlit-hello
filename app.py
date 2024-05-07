import streamlit as st
import pandas as pd
import numpy as np
import csv
import datetime
import requests
import io

@st.cache_data
def fetch_data():
    dataurl = "https://www.immd.gov.hk/opendata/eng/transport/immigration_clearance/statistics_on_daily_passenger_traffic.csv"
    response = requests.get(dataurl)
    with open('local_data.csv', 'wb') as file:
        file.write(response.content)
    data = pd.read_csv('local_data.csv')
    data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
    return data

df = fetch_data()

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# Adjust values to negative for 'Departure' type in specified columns
departure_columns = ['Hong Kong Residents', 'Mainland Visitors', 'Other Visitors']
df.loc[df['Arrival / Departure'] == 'Departure', departure_columns] *= -1

# Aggregate data by date
aggregated_data = df.groupby('Date')[departure_columns].sum()

# group data by control points 
control_points = df['Control Point'].unique()
control_points_data = {control_point: df[df['Control Point'] == control_point] for control_point in control_points}

# Filter data for the years 2021 to 2024
data_2021 = aggregated_data[aggregated_data.index.year == 2021]
data_2022 = aggregated_data[aggregated_data.index.year == 2022]
data_2023 = aggregated_data[aggregated_data.index.year == 2023]
data_2024 = aggregated_data[aggregated_data.index.year == 2024]

# Visualize data

st.title("Daily Passenger Traffic of all border control points from 2021 to 2024")

st.header("Daily Passenger Traffic of 2021 to 2024")

st.subheader("Daily Passenger Traffic of 2021 to 2024")

st.write("This is the daily passenger traffic of all border control points from 2021 to 2024. The border between China Hong Kong opened on 2023-02-06.")
st.bar_chart(aggregated_data[departure_columns])

st.subheader("Daily Passenger Traffic of 2021")
st.bar_chart(data_2021[departure_columns])
st.divider()
st.subheader("Daily Passenger Traffic of 2022")
st.bar_chart(data_2022[departure_columns])
st.divider()
st.subheader("Daily Passenger Traffic of 2023")
st.bar_chart(data_2023[departure_columns])
st.divider()
st.subheader("Daily Passenger Traffic of 2024")
st.bar_chart(data_2024[departure_columns])
st.divider()
st.dataframe(aggregated_data)
