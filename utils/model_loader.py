import joblib
import streamlit as st

@st.cache_resource
def load_models():

    classifier = joblib.load("models/delay_classifier.pkl")
    regressor = joblib.load("models/delay_regressor.pkl")
    features = joblib.load("models/feature_names.pkl")

    return classifier, regressor, features