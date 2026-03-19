import pandas as pd
import streamlit as st


@st.cache_data
def load_raw_tables():

    airlines = pd.read_csv("data/airlines.csv")
    airports = pd.read_csv("data/airports.csv")
    routes = pd.read_csv("data/routes.csv")
    flights = pd.read_csv("data/merge_flights.csv")
    delays = pd.read_csv("data/delays.csv")
    weather = pd.read_csv("data/weather.csv")

    return airlines, airports, routes, flights, delays, weather


@st.cache_data
def load_master_dataset():

    airlines, airports, routes, flights, delays, weather = load_raw_tables()

    df = flights.merge(airlines, on="airline_id", how="left")

    df = df.merge(routes, on="route_id", how="left")

    origin_airports = airports.rename(columns={
        "airport_id":"origin_airport_id",
        "airport_code":"origin_airport_code",
        "airport_name":"origin_airport_name",
        "city":"origin_city",
        "state":"origin_state",
        "country":"origin_country",
        "latitude":"origin_latitude",
        "longitude":"origin_longitude",
        "total_passengers_boarding":"origin_passenger_volume"
    })

    df = df.merge(origin_airports, on="origin_airport_id", how="left")

    dest_airports = airports.rename(columns={
        "airport_id":"destination_airport_id",
        "airport_code":"destination_airport_code",
        "airport_name":"destination_airport_name",
        "city":"destination_city",
        "state":"destination_state",
        "country":"destination_country"
    })

    df = df.merge(dest_airports, on="destination_airport_id", how="left")

    df.rename(columns={
    "delay_minutes_x": "delay_minutes",
    "delay_minutes_y": "delay_minutes_detail"
    }, inplace=True)

    df["scheduled_departure_time"] = pd.to_datetime(df["scheduled_departure_time"])
    df["scheduled_departure_date"] = pd.to_datetime(df["scheduled_departure_date"])

    df["departure_hour"] = df["scheduled_departure_time"].dt.hour
    df["day_of_week"] = df["scheduled_departure_date"].dt.dayofweek + 1
    df["month"] = df["scheduled_departure_date"].dt.month

    weather["date_time"] = pd.to_datetime(weather["date_time"])
    weather["weather_date"] = weather["date_time"].dt.date

    df["flight_date"] = df["scheduled_departure_date"].dt.date

    df = df.merge(
        weather,
        left_on=["origin_airport_id","flight_date"],
        right_on=["airport_id","weather_date"],
        how="left"
    )

    def distance_category(distance):

        if distance < 500:
            return "Short Haul"

        elif distance <= 1500:
            return "Medium Haul"

        else:
            return "Long Haul"

    df["distance_category"] = df["distance_miles"].apply(distance_category)

    return df