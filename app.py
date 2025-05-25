import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import streamlit.components.v1 as components

# Configure Streamlit page
st.set_page_config(
    page_title="CitiBike Dashboard",
    page_icon="🚲",
    layout="wide"
)

st.title("🚲 CitiBike Dashboard")
st.markdown("""
Welcome to the CitiBike data dashboard!  
This app visualizes NYC CitiBike trips including the most popular start stations,  
daily trip trends, and a map of bike trip locations using kepler.gl.
""")

# Load data
df = pd.read_csv("/Users/alden/citibike_tripdata_cleaned.csv", dtype={'start_station_id': str})

# Top 10 start stations
top_stations = df['start_station_name'].value_counts().nlargest(10).reset_index()
top_stations.columns = ['Station', 'Trips']
fig1 = px.bar(top_stations, x='Station', y='Trips', title='Top 10 Most Popular Start Stations')

# Daily trip counts
df['date'] = pd.to_datetime(df['started_at']).dt.date
daily_trips = df.groupby('date').size().reset_index(name='trip_count')

# Add fake temperature data
daily_trips['temperature'] = [random.uniform(5, 25) for _ in range(len(daily_trips))]

# Dual-axis plot: Trips and Temperature
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=daily_trips['date'], y=daily_trips['trip_count'], name='Trips', yaxis='y1'))
fig2.add_trace(go.Scatter(x=daily_trips['date'], y=daily_trips['temperature'], name='Temperature (°C)', yaxis='y2'))
fig2.update_layout(
    title='Trips and Temperature Over Time',
    yaxis=dict(title='Trips'),
    yaxis2=dict(title='Temperature (°C)', overlaying='y', side='right')
)

# Load Kepler.gl map
with open("Kepler.gl.html", 'r') as f:
    html_data = f.read()

# Display everything
st.subheader("Top 10 Most Popular Start Stations")
st.plotly_chart(fig1)

st.subheader("Daily Trips vs Temperature")
st.plotly_chart(fig2)

st.subheader("Bike Trips Map")
components.html(html_data, height=600)
