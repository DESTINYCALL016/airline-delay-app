import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_master_dataset

df = load_master_dataset()

st.title("✈ Flight Operations Overview")
st.write("Operational snapshot of airline activity and delay performance")

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


total_flights = df["flight_id"].nunique()

on_time = df[(df["flight_status"] == "On Time") & (df["delay_minutes"].le(15))].shape[0]
on_time_pct = round((on_time / total_flights) * 100, 2)

avg_delay = round(df[df["flight_status"] == "Delayed"]["delay_minutes"].mean(), 2)

cancelled = df[df["flight_status"] == "Cancelled"].shape[0]
cancel_rate = round((cancelled / total_flights) * 100, 2)

diverted = df[df["flight_status"] == "Diverted"].shape[0]
divert_rate = round((diverted / total_flights) * 100, 2)

k1,k2,k3,k4,k5 = st.columns(5)

k1.metric("✈ Total Flights", f"{total_flights:,}")
k2.metric("⏱ On-Time Performance", f"{on_time_pct}%")
k3.metric("⏳ Avg Delay (min)", avg_delay)
k4.metric("❌ Cancellation Rate", f"{cancel_rate}%")
k5.metric("🔀 Diversion Rate", f"{divert_rate}%")

st.markdown("---")

airline_counts = (
    df.groupby("airline_name")["flight_id"]
    .count()
    .reset_index()
    .sort_values("flight_id", ascending=False)
)

fig_airline = px.bar(
    airline_counts,
    x="airline_name",
    y="flight_id",
    title="Flights by Airline",
    color="flight_id",
)

fig_airline.update_layout(
    xaxis_title="Airline",
    yaxis_title="Number of Flights"
)


airport_counts = (
    df.groupby("origin_airport_code")["flight_id"]
    .count()
    .reset_index()
    .sort_values("flight_id", ascending=False)
)

fig_airport = px.bar(
    airport_counts.head(15),
    x="origin_airport_code",
    y="flight_id",
    title="Top Airports by Flight Volume",
    color="flight_id"
)


status_counts = (
    df.groupby("flight_status")["flight_id"]
    .count()
    .reset_index()
)

fig_status = px.pie(
    status_counts,
    values="flight_id",
    names="flight_status",
    hole=0.5,
    title="Flight Status Distribution"
)


delay_hour = df.groupby("departure_hour")["delay_minutes"].mean().reset_index()

fig_hour = px.line(
    delay_hour,
    x="departure_hour",
    y="delay_minutes",
    title="Average Delay by Departure Hour",
    markers=True
)


delay_hour = (
    df.groupby("departure_hour")["delay_minutes"]
    .mean()
    .reset_index()
)

fig_hour = px.line(
    delay_hour,
    x="departure_hour",
    y="delay_minutes",
    title="Average Delay by Departure Hour",
    markers=True
)

fig_hour.update_layout(
    xaxis_title="Departure Hour",
    yaxis_title="Average Delay (Minutes)"
)

heatmap_data = (
    df.groupby(["day_of_week","departure_hour"])["delay_minutes"]
    .mean()
    .reset_index()
)

fig_heatmap = px.density_heatmap(
    heatmap_data,
    x="departure_hour",
    y="day_of_week",
    z="delay_minutes",
    title="Delay Heatmap (Day vs Hour)"
)

fig_heatmap.update_layout(
    xaxis_title="Departure Hour",
    yaxis_title="Day of Week"
)

c1,c2 = st.columns(2)

with c1:
    st.plotly_chart(fig_airline, use_container_width=True)

with c2:
    st.plotly_chart(fig_airport, use_container_width=True)

c3,c4 = st.columns(2)

with c3:
    st.plotly_chart(fig_status, use_container_width=True)

with c4:
    st.plotly_chart(fig_hour, use_container_width=True)

st.plotly_chart(fig_heatmap, use_container_width=True)