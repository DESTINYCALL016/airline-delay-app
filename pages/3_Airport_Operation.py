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

month_filter = st.sidebar.selectbox(
    "Month",
    ["All"] + sorted(df["month"].dropna().unique())
)

# Apply filters

if airline_filter != "All":
    df = df[df["airline_name"] == airline_filter]

if month_filter != "All":
    df = df[df["month"] == month_filter]

st.title("🛫 Airport Operations Dashboard")
st.caption("Airport congestion, delay patterns, and traffic distribution")

airport_stats = (
    df.groupby("origin_airport_code")
    .agg(
        total_flights=("flight_id","count"),
        avg_delay=("delay_minutes","mean"),
        passenger_volume=("origin_passenger_volume","mean"),
        delayed=("flight_status", lambda x: (x=="Delayed").sum())
    )
    .reset_index()
)

airport_stats["delay_rate"] = round(
    airport_stats["delayed"] / airport_stats["total_flights"] * 100,2
)

total_airports = airport_stats["origin_airport_code"].nunique()

total_flights = airport_stats["total_flights"].sum()

avg_airport_delay = round(airport_stats["avg_delay"].mean(),2)

worst_airport = airport_stats.sort_values(
    "avg_delay",ascending=False
).iloc[0]["origin_airport_code"]

avg_passengers = int(airport_stats["passenger_volume"].mean())

k1,k2,k3,k4,k5 = st.columns(5)

k1.metric("🛫 Airports", total_airports)
k2.metric("✈ Flights", f"{total_flights:,}")
k3.metric("⏳ Avg Airport Delay", avg_airport_delay)
k4.metric("⚠ Highest Delay Airport", worst_airport)
k5.metric("👥 Avg Passenger Volume", f"{avg_passengers:,}")

fig_traffic = px.bar(
    airport_stats.sort_values("total_flights",ascending=False).head(20),
    x="origin_airport_code",
    y="total_flights",
    title="Top Airports by Flight Traffic",
    color="total_flights"
)

fig_delay = px.bar(
    airport_stats.sort_values("avg_delay",ascending=False).head(20),
    x="origin_airport_code",
    y="avg_delay",
    title="Airports with Highest Average Delay",
    color="avg_delay"
)

fig_congestion = px.scatter(
    airport_stats,
    x="passenger_volume",
    y="avg_delay",
    size="total_flights",
    hover_name="origin_airport_code",
    title="Passenger Volume vs Delay (Airport Congestion)"
)

fig_delay_rate = px.bar(
    airport_stats.sort_values("delay_rate",ascending=False).head(20),
    x="origin_airport_code",
    y="delay_rate",
    title="Delay Rate by Airport (%)",
    color="delay_rate"
)

c1,c2 = st.columns(2)

with c1:
    st.plotly_chart(fig_traffic, use_container_width=True)

with c2:
    st.plotly_chart(fig_delay, use_container_width=True)

c3,c4 = st.columns(2)

with c3:
    st.plotly_chart(fig_congestion, use_container_width=True)

with c4:
    st.plotly_chart(fig_delay_rate, use_container_width=True)