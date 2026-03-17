import streamlit as st
import pandas as pd
import joblib

classifier = joblib.load("models/delay_classifier.pkl")
regressor = joblib.load("models/delay_regressor.pkl")
features = joblib.load("models/feature_names.pkl")

st.title("🤖 Flight Delay Prediction")
st.caption("Simulate flight scenarios and estimate delay probability")

st.markdown("### ✈ Flight Scenario Simulator")

c1,c2,c3 = st.columns(3)



with c1:
    departure_hour = st.slider("Departure Hour",0,23,12)

    day_of_week = st.selectbox(
        "Day of Week",
        [1,2,3,4,5,6,7]
    )

    month = st.selectbox(
        "Month",
        list(range(1,13))
    )

with c2:
    passenger_volume = st.number_input(
        "Origin Passenger Volume",
        value=5000000
    )

    distance_miles = st.slider(
        "Route Distance (Miles)",
        50,5000,800
    )

with c3:
    temperature = st.slider(
        "Temperature (°C)",
        -10,45,20
    )

    wind_speed = st.slider(
        "Wind Speed (km/h)",
        0,80,10
    )

    visibility = st.slider(
        "Visibility (km)",
        0,10,8
    )

    precipitation = st.slider(
        "Precipitation (mm)",
        0,50,0
    )
st.markdown("---")

predict = st.button("Predict Delay")

if predict:

    input_data = pd.DataFrame([{
        "departure_hour": departure_hour,
        "day_of_week": day_of_week,
        "month": month,
        "origin_passenger_volume": passenger_volume,
        "distance_miles": distance_miles,
        "temperature": temperature,
        "wind_speed": wind_speed,
        "visibility": visibility,
        "precipitation": precipitation
    }])

    delay_prob = classifier.predict_proba(input_data)[0][1]

    delay_minutes = regressor.predict(input_data)[0]

    if delay_prob < 0.3:
        risk = "Low Risk 🟢"
    elif delay_prob < 0.6:
        risk = "Moderate Risk 🟡"
    else:
        risk = "High Risk 🔴"

    st.markdown("### Prediction Results")

    c1, c2, c3 = st.columns(3)

    c1.metric("Delay Probability", f"{delay_prob*100:.1f}%")
    c2.metric("Expected Delay", f"{delay_minutes:.1f} minutes")
    c3.metric("Risk Level", risk)

    st.progress(float(delay_prob))