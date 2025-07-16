
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Citi Bike Dashboard", layout="wide")

@st.cache_data
def load_data():
    trips_weather = pd.read_csv("daily_trips_weather.csv", parse_dates=["date"])
    kepler_map_html = open("kepler_map.html", "r").read()
    station_data = pd.read_csv("kepler_ready_sample.csv")
    return trips_weather, kepler_map_html, station_data

trips_weather, kepler_map_html, station_data = load_data()

st.sidebar.header("🔍 Filter Data")
season_filter = st.sidebar.selectbox("Select Season", ["All"] + sorted(station_data["season"].dropna().unique()))

if season_filter != "All":
    trips_weather = trips_weather[trips_weather["season"] == season_filter]
    station_data = station_data[station_data["season"] == season_filter]

tabs = st.tabs(["🏠 Home", "📈 Trips vs Temp", "🗺️ Kepler Map", "📍 Top Stations", "💡 Recommendations"])

# --- HOME ---
with tabs[0]:
    st.title("🚲 Citi Bike Data Dashboard")
    st.markdown("""
    Welcome to the NYC Citi Bike Dashboard! This tool allows you to explore how **bike trips** and **weather** interact across seasons in NYC.

    ### 📂 Data Sources:
    - `daily_trips_weather.csv`: Trip counts + weather by day
    - `kepler_map.html`: Kepler.gl map of trip densities
    - `kepler_ready_sample.csv`: Station-level trips with coordinates and names

    ### 📊 Dashboard Tabs:
    - **Trips vs Temp**: Line chart of trip activity vs. temperature
    - **Kepler Map**: Interactive spatial heatmap
    - **Top Stations**: Charts and map of most used stations
    - **Recommendations**: Strategy tips based on insights

    Use the **sidebar** to filter by season.
    """)

# --- TRIPS VS TEMP ---
with tabs[1]:
    st.subheader("📈 Trips vs Temperature")
    try:
        fig, ax1 = plt.subplots(figsize=(12, 5))
        ax2 = ax1.twinx()
        sns.lineplot(data=trips_weather, x="date", y="trip_count", ax=ax1, color="blue")
        sns.lineplot(data=trips_weather, x="date", y="avg_temp_f", ax=ax2, color="red")
        ax1.set_ylabel("Trip Count", color="blue")
        ax2.set_ylabel("Avg Temp (°F)", color="red")
        ax1.set_xlabel("Date")
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True)
        st.pyplot(fig)
        st.markdown("""
        _We observe a clear seasonal trend:_
        - 🚴‍♂️ **Higher trip volumes** during warm months (peak in summer)
        - ❄️ **Lower usage** in colder months
        """)
    except Exception as e:
        st.exception(e)

# --- KEPLER MAP ---
with tabs[2]:
    st.subheader("🗺️ Kepler Map: Spatial Trip Activity")
    st.markdown("""
    This interactive map, powered by Kepler.gl, shows spatial patterns of bike trip activity across NYC.

    ### 🔍 How to Use:
    - **Zoom** and **pan** to inspect activity across neighborhoods
    - Use **season filter** (left sidebar) to observe how usage changes throughout the year
    - Lighter areas indicate **higher trip densities**

    💡 For most detailed exploration of spatial patterns, this map is your best tool.
    """)
    try:
        components.html(kepler_map_html, height=600)
    except Exception as e:
        st.exception(e)

# --- TOP STATIONS ---
with tabs[3]:
    st.subheader("📍 Top Stations by Trip Count")
    try:
        top = station_data["start_station_name"].value_counts().reset_index()
        top.columns = ["Station Name", "Trip Count"]
        top10 = top.head(10)

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=top10, x="Trip Count", y="Station Name", palette="mako", ax=ax)
        ax.set_title("Top 10 Stations by Trip Count")
        st.pyplot(fig)

        st.markdown("""
        This chart highlights the most active Citi Bike stations based on total ride volume.

        ### 🧭 What we observe:
        - Stations with the highest trip counts are typically near:
            - 🚇 Transit hubs
            - 🏙️ Commercial zones
            - 🧭 Tourist corridors
        - Seasonal filtering reveals changing patterns: some stations surge in summer while others are consistent year-round.
        """)

        st.subheader("📌 Top 10 Station Locations (Interactive Map)")
        top_station_names = top10["Station Name"].tolist()
        top_coords = station_data[station_data["start_station_name"].isin(top_station_names)]
        coord_grouped = top_coords.groupby("start_station_name")[["start_lat", "start_lng"]].mean().reset_index()

        folium_map = folium.Map(location=[40.75, -73.98], zoom_start=12)
        marker_cluster = MarkerCluster().add_to(folium_map)

        for _, row in coord_grouped.iterrows():
            folium.Marker(
                location=[row["start_lat"], row["start_lng"]],
                popup=row["start_station_name"],
                tooltip=row["start_station_name"]
            ).add_to(marker_cluster)

        st_folium(folium_map, width=700, height=500)

    except Exception as e:
        st.exception(e)

# --- RECOMMENDATIONS ---
with tabs[4]:
    st.subheader("💡 Strategic Recommendations")
    st.markdown("""
    Based on usage trends and weather patterns:

    - 🚴‍♀️ Increase **bike availability** in summer months
    - 🚚 Deploy **extra bikes** to high-demand stations during peak times
    - 🛠️ Adjust **maintenance schedules** by season to match demand
    - 🤖 Future enhancement: Use ML to predict station-level demand and automate rebalancing
    """)
