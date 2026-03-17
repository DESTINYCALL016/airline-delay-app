import streamlit as st
from utils.auth import login_page

st.markdown("""
<style>

body {
background-color:#0E1117;
}

[data-testid="stMetricValue"] {
font-size:28px;
font-weight:bold;
}

[data-testid="stSidebar"] {
background-color:#1C1F26;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Airline Delay Intelligence Hub",
    page_icon="✈",
    layout="wide"
)

# Session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# LOGIN PAGE
if not st.session_state.authenticated:
    login_page()

# DASHBOARD
else:

    st.sidebar.success("Logged in")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    st.title("✈ Airline Delay Intelligence Hub")

    st.markdown("""
Operational Analytics for **Flight Delay Risk Management**

Use the sidebar to navigate through dashboards.

• Overview  
• Airline Performance  
• Airport Operations  
• Route Network  
• Weather Impact  
• Delay Prediction
""")