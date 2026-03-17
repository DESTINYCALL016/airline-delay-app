import streamlit as st
import plotly.express as px
from utils.data_loader import load_master_dataset

df = load_master_dataset()

st.title("✈ Airline Performance Analysis")
st.caption("Comparison of airline reliability, delay patterns, and operational efficiency")


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

airline_stats = (
    df.groupby("airline_name")
    .agg(
        total_flights=("flight_id","count"),
        avg_delay=("delay_minutes","mean"),
        cancelled=("flight_status", lambda x: (x=="Cancelled").sum()),
        diverted=("flight_status", lambda x: (x=="Diverted").sum()),
        on_time=("flight_status", lambda x: (x=="On Time").sum())
    )
    .reset_index()
)

airline_stats["on_time_pct"] = round(
    airline_stats["on_time"] / airline_stats["total_flights"] * 100, 2
)

airline_stats["cancel_rate"] = round(
    airline_stats["cancelled"] / airline_stats["total_flights"] * 100, 2
)

airline_stats["reliability_score"] = round(
    airline_stats["on_time_pct"] / airline_stats["avg_delay"], 2
)

# KPI Calculations
total_airlines = airline_stats["airline_name"].nunique()

total_flights = airline_stats["total_flights"].sum()

best_airline = airline_stats.sort_values(
    "on_time_pct", ascending=False
).iloc[0]["airline_name"]

worst_airline = airline_stats.sort_values(
    "avg_delay", ascending=False
).iloc[0]["airline_name"]

avg_airline_delay = round(airline_stats["avg_delay"].mean(), 2)

k1,k2,k3,k4,k5 = st.columns(5)

k1.metric("🏢 Airlines", total_airlines)
k2.metric("✈ Flights Analyzed", f"{total_flights:,}")
k3.metric("🥇 Best On-Time Airline", best_airline)
k4.metric("⚠ Worst Delay Airline", worst_airline)
k5.metric("⏳ Avg Airline Delay", avg_airline_delay)

st.markdown("---")

fig_ontime = px.bar(
    airline_stats.sort_values("on_time_pct",ascending=False),
    x="airline_name",
    y="on_time_pct",
    title="Airline On-Time Performance (%)",
    color="on_time_pct"
)

fig_delay = px.bar(
    airline_stats.sort_values("avg_delay",ascending=False),
    x="airline_name",
    y="avg_delay",
    title="Average Delay by Airline",
    color="avg_delay"
)

fig_cancel = px.bar(
    airline_stats.sort_values("cancel_rate",ascending=False),
    x="airline_name",
    y="cancel_rate",
    title="Cancellation Rate by Airline",
    color="cancel_rate"
)

fig_reliability = px.bar(
    airline_stats.sort_values("reliability_score",ascending=False),
    x="airline_name",
    y="reliability_score",
    title="Airline Reliability Score",
    color="reliability_score"
)

delay_causes = (
    df.groupby(["airline_name","delay_type"])["flight_id"]
    .count()
    .reset_index()
)


fig_delay_type = px.bar(
    delay_causes,
    x="airline_name",
    y="flight_id",
    color="delay_type",
    title="Delay Causes by Airline"
)

c1,c2 = st.columns(2)

with c1:
    st.plotly_chart(fig_ontime, use_container_width=True)

with c2:
    st.plotly_chart(fig_delay, use_container_width=True)

c3,c4 = st.columns(2)

with c3:
    st.plotly_chart(fig_cancel, use_container_width=True)

with c4:
    st.plotly_chart(fig_reliability, use_container_width=True)

st.plotly_chart(fig_delay_type, use_container_width=True)