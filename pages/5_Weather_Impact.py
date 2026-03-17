import streamlit as st
import plotly.express as px
from utils.data_loader import load_master_dataset

df = load_master_dataset()

# ---------------- SLICERS ----------------

st.sidebar.header("Dashboard Filters")

airline_filter = st.sidebar.selectbox(
    "Select Airline",
    ["All"] + sorted(df["airline_name"].dropna().unique())
)

origin_filter = st.sidebar.selectbox(
    "Origin Airport",
    ["All"] + sorted(df["origin_airport_code"].dropna().unique())
)

month_filter = st.sidebar.selectbox(
    "Month",
    ["All"] + sorted(df["month"].dropna().unique())
)

# Apply Filters

if airline_filter != "All":
    df = df[df["airline_name"] == airline_filter]

if origin_filter != "All":
    df = df[df["origin_airport_code"] == origin_filter]

if month_filter != "All":
    df = df[df["month"] == month_filter]

st.title("🌦 Weather Impact Dashboard")
st.caption("Analyze how weather conditions influence flight delays")

weather_stats = (
    df.groupby("conditions")
    .agg(
        total_flights=("flight_id","count"),
        avg_delay=("delay_minutes","mean"),
        avg_temp=("temperature","mean"),
        avg_wind=("wind_speed","mean"),
        avg_visibility=("visibility","mean"),
        avg_precip=("precipitation","mean")
    )
    .reset_index()
)

total_weather_types = weather_stats["conditions"].nunique()

avg_weather_delay = round(weather_stats["avg_delay"].mean(),2) if not weather_stats.empty else 0

if not weather_stats.empty:
    
    worst_weather = weather_stats.sort_values(
        "avg_delay", ascending=False
    ).iloc[0]["conditions"]

else:
    
    worst_weather = "No Data"

avg_wind = round(df["wind_speed"].mean(),2)

avg_visibility = round(df["visibility"].mean(),2)

k1,k2,k3,k4,k5 = st.columns(5)

k1.metric("🌤 Weather Types", total_weather_types)
k2.metric("⏳ Avg Delay (Weather)", avg_weather_delay)
k3.metric("⚠ Worst Condition", worst_weather)
k4.metric("💨 Avg Wind Speed", avg_wind)
k5.metric("👁 Avg Visibility", avg_visibility)

fig_weather_delay = px.bar(
    weather_stats,
    x="conditions",
    y="avg_delay",
    title="Average Delay by Weather Condition",
    color="avg_delay"
)

fig_temp_delay = px.scatter(
    df,
    x="temperature",
    y="delay_minutes",
    title="Temperature vs Flight Delay",
    opacity=0.6
)

fig_wind_delay = px.scatter(
    df,
    x="wind_speed",
    y="delay_minutes",
    title="Wind Speed vs Delay",
    opacity=0.6
)

fig_visibility_delay = px.scatter(
    df,
    x="visibility",
    y="delay_minutes",
    title="Visibility vs Delay",
    opacity=0.6
)

fig_precip_delay = px.scatter(
    df,
    x="precipitation",
    y="delay_minutes",
    title="Precipitation vs Delay",
    opacity=0.6
)

c1,c2 = st.columns(2)

with c1:
    st.plotly_chart(fig_weather_delay, use_container_width=True)

with c2:
    st.plotly_chart(fig_temp_delay, use_container_width=True)

c3,c4 = st.columns(2)

with c3:
    st.plotly_chart(fig_wind_delay, use_container_width=True)

with c4:
    st.plotly_chart(fig_visibility_delay, use_container_width=True)

st.plotly_chart(fig_precip_delay, use_container_width=True)