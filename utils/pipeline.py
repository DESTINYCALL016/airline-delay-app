import pandas as pd
import joblib


def run_full_pipeline():

    # STEP 1: Load data (replace with your real updated dataset)
    df = pd.read_csv("data/merge_flights.csv")

    # STEP 2: Feature engineering
    df["scheduled_departure_time"] = df["scheduled_departure_time"].astype(str)

    df["departure_hour"] = (
        df["scheduled_departure_time"]
        .str.split(":").str[0]
        .astype(int) % 24
    )

    df["day_of_week"] = pd.to_datetime(df["scheduled_departure_date"]).dt.dayofweek + 1
    df["month"] = pd.to_datetime(df["scheduled_departure_date"]).dt.month

    # Dummy values if not present (for safety)
    df["origin_passenger_volume"] = 5000000
    df["temperature"] = 20
    df["wind_speed"] = 10
    df["visibility"] = 8
    df["precipitation"] = 0

    # STEP 3: Load models
    classifier = joblib.load("models/delay_classifier.pkl")
    regressor = joblib.load("models/delay_regressor.pkl")

    # STEP 4: Select features
    features = [
        'departure_hour',
        'day_of_week',
        'month',
        'origin_passenger_volume',
        'distance_miles',
        'temperature',
        'wind_speed',
        'visibility',
        'precipitation'
    ]

    X = df[features]

    # STEP 5: Predictions
    df["delay_probability"] = classifier.predict_proba(X)[:, 1]
    df["predicted_delay_minutes"] = regressor.predict(X)

    # STEP 6: Save output
    df.to_csv("data/predictions.csv", index=False)

    return "Pipeline executed successfully"


# Required for scheduler
if __name__ == "__main__":
    run_full_pipeline()