# 🚴 Citi Bike Data Dashboard

An interactive Streamlit dashboard to explore NYC Citi Bike usage and weather trends by season.

## 🔗 Live Demo
👉 [View the live dashboard](https://citi-bike-project-wzrs9qpcxloasag28psvfb.streamlit.app/)

## 📊 Features

- Seasonal filter (Spring, Summer, Fall, Winter)
- **Trips vs Temp**: Line chart of trip count vs temperature
- **Kepler Map**: Interactive spatial map of bike trips
- **Top Stations**: Charts + Folium map of top-used stations
- **Recommendations**: Strategy tips based on data insights

## 📁 Files

| File                    | Purpose                                         |
|-------------------------|-------------------------------------------------|
| `app.py`                | Streamlit dashboard app                         |
| `daily_trips_weather.csv` | Weather + trip data by day                   |
| `kepler_map.html`       | Kepler.gl map HTML for spatial visualization   |
| `kepler_ready_sample.csv` | Station-level trip data with coordinates    |

## ▶️ Running Locally

Clone the repo and install dependencies:

```bash
git clone https://github.com/AldenMedina/citi-bike-project.git
cd citi-bike-project
pip install -r requirements.txt
streamlit run app.py
