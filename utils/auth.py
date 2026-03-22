import streamlit as st


def login_page():

    # ✅ Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # ✅ Styling
    st.markdown(
        """
        <style>
        .login-container {
            background-color: #1C1F26;
            padding: 40px;
            border-radius: 15px;
            width: 400px;
            margin: auto;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ✅ Header
    st.markdown("<h1 style='text-align:center;'>✈ Airline Intelligence Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Flight Delay Analytics Dashboard</h4>", unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")

        login_clicked = st.button("Login", use_container_width=True)

        if login_clicked:

            if username == "admin" and password == "admin123":

                st.session_state.authenticated = True
                st.success("Login successful")

                # ✅ Safe rerun
                st.experimental_rerun()

            else:
                st.error("Invalid username or password")

    return st.session_state.authenticated