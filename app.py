import streamlit as st

# ✅ MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Airline Delay Intelligence Hub",
    page_icon="✈",
    layout="wide"
)

from utils.auth import login_page
from utils.pipeline import run_full_pipeline

# ✅ Session state init
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# ================= LOGIN =================
if not st.session_state.authenticated:

    login_page()
    st.stop()   # 🚨 VERY IMPORTANT


# ================= MAIN APP =================

# 🎨 Styling
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


# ================= SIDEBAR =================

st.sidebar.success("Logged in")

# 🔄 Pipeline Button
st.sidebar.markdown("---")
st.sidebar.subheader("⚙ Admin Panel")

if st.sidebar.button("🔄 Refresh Data & Model"):

    with st.spinner("Running pipeline..."):
        result = run_full_pipeline()

    st.sidebar.success(result)


# 🔓 Logout
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.experimental_rerun()


# ================= MAIN CONTENT =================

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