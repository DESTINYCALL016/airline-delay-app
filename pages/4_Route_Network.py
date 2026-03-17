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

# Apply filters

if airline_filter != "All":
    df = df[df["airline_name"] == airline_filter]

if origin_filter != "All":
    df = df[df["origin_airport_code"] == origin_filter]

if month_filter != "All":
    df = df[df["month"] == month_filter]

st.title("🗺 Route Network Dashboard")
st.caption("Route performance, distance impact, and delay-prone routes")

df["route"] = df["origin_airport_code"] + " → " + df["destination_airport_code"]

route_stats = (
    df.groupby("route")
    .agg(
        total_flights=("flight_id","count"),
        avg_delay=("delay_minutes","mean"),
        avg_distance=("distance_miles","mean"),
        delayed=("flight_status", lambda x: (x=="Delayed").sum())
    )
    .reset_index()
)

route_stats["delay_rate"] = round(
    route_stats["delayed"] / route_stats["total_flights"] * 100,2
)

total_routes = route_stats["route"].nunique()

avg_route_delay = round(route_stats["avg_delay"].mean(),2)

longest_route = route_stats.sort_values(
    "avg_distance",ascending=False
).iloc[0]["route"]

worst_route = route_stats.sort_values(
    "avg_delay",ascending=False
).iloc[0]["route"]

avg_distance = int(route_stats["avg_distance"].mean())

k1,k2,k3,k4,k5 = st.columns(5)

k1.metric("🗺 Routes", total_routes)
k2.metric("⏳ Avg Route Delay", avg_route_delay)
k3.metric("📏 Avg Route Distance", avg_distance)
k4.metric("⚠ Highest Delay Route", worst_route)
k5.metric("🛫 Longest Route", longest_route)

fig_route_traffic = px.bar(
    route_stats.sort_values("total_flights",ascending=False).head(20),
    x="route",
    y="total_flights",
    title="Top Routes by Flight Volume",
    color="total_flights"
)

fig_route_delay = px.bar(
    route_stats.sort_values("avg_delay",ascending=False).head(20),
    x="route",
    y="avg_delay",
    title="Routes with Highest Average Delay",
    color="avg_delay"
)

fig_distance_delay = px.scatter(
    route_stats,
    x="avg_distance",
    y="avg_delay",
    size="total_flights",
    hover_name="route",
    title="Route Distance vs Delay"
)

fig_delay_rate = px.bar(
    route_stats.sort_values("delay_rate",ascending=False).head(20),
    x="route",
    y="delay_rate",
    title="Routes with Highest Delay Rate (%)",
    color="delay_rate"
)

c1,c2 = st.columns(2)

with c1:
    st.plotly_chart(fig_route_traffic, use_container_width=True)

with c2:
    st.plotly_chart(fig_route_delay, use_container_width=True)

c3,c4 = st.columns(2)

with c3:
    st.plotly_chart(fig_distance_delay, use_container_width=True)

with c4:
    st.plotly_chart(fig_delay_rate, use_container_width=True)