import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Electrical Demand Forecast Dashboard",
    page_icon="⚡",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "page" not in st.session_state:
    st.session_state.page = "home"

# ==================================================
# DARK MODE
# ==================================================

dark_mode = st.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)

st.session_state.dark_mode = dark_mode

bg_color = "#0E1117" if dark_mode else "white"
font_color = "white" if dark_mode else "black"
chart_theme = "plotly_dark" if dark_mode else "plotly_white"

# ==================================================
# DARK MODE CSS
# ==================================================

if dark_mode:

    st.markdown("""
    <style>

    .stApp {
        background-color:#0E1117;
        color:white;
    }

    h1,h2,h3,h4,h5,h6,p {
        color:white !important;
    }

    .stSelectbox div[data-baseweb="select"]{
        color:black !important;
    }

    .stDateInput input{
        color:black !important;
    }

    </style>
    """, unsafe_allow_html=True)

# ==================================================
# GENERAL CSS
# ==================================================

st.markdown("""
<style>

/* MAIN TITLE */
.main-title{
    text-align:center;
    font-size:72px;
    font-weight:700;
}

/* HOME CARDS */

div[data-testid="stButton"] button {
    height:120px;
    font-size:22px;
    font-weight:600;
    border-radius:12px;
}

/* METRICS */

[data-testid="stMetricValue"]{
    font-size:34px;
}

/* CENTER RADIOS */

div[role="radiogroup"]{
    display:flex;
    justify-content:center;
    gap:50px;
}

/* GREEN BUTTONS */

.stButton button{
    background-color:#4CAF50;
    color:white;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA
# ==================================================

data = pd.read_csv("demand_data.csv")

data["Date"] = pd.to_datetime(
    data["Date"],
    errors="coerce"
)

# ==================================================
# HEADER ALWAYS VISIBLE
# ==================================================

st.markdown(
"""
<div class='main-title'>
Electrical Demand Forecast Dashboard
</div>
""",
unsafe_allow_html=True
)

# ==================================================
# HOME PAGE
# ==================================================

if st.session_state.page == "home":

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):

        st.markdown(
        """
        <div style='text-align:center;
                    font-size:20px;
                    line-height:1.5;'>

        Cloud-hosted dashboard for provincial and
        postal code demand forecasting.

        <br>

        A Capstone Project By:
        Syed AbdulRahman • Soomin Maeng •
        Ammar Abou Elmorin • Omar Farag

        <br><br>

        <div style='font-size:30px;
                    font-weight:600;'>

        Welcome to the Canadian Electrical Demand Dashboard

        </div>

        Please select Provincial Demand
        or Postal Code Demand to begin forecasting.

        </div>
        """,
        unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🏛 Provincial Demand Dashboard",
            use_container_width=True
        ):
            st.session_state.page = "provincial"
            st.rerun()

    with col2:

        if st.button(
            "📮 Postal Code Demand Dashboard",
            use_container_width=True
        ):
            st.session_state.page = "postal"
            st.rerun()

# ==================================================
# PROVINCIAL PAGE
# ==================================================

elif st.session_state.page == "provincial":

    if st.button("← Return Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown(
        "<h1 style='text-align:center;'>Canadian Provinces</h1>",
        unsafe_allow_html=True
    )

    mode = st.radio(
        "",
        ["Historical Demand", "Forecast Demand"],
        horizontal=True
    )

    # ======================================

    with st.container(border=True):

        if mode == "Historical Demand":

            st.write(
                "Select your province and date range "
                "to generate historical demand."
            )

            province = st.selectbox(
                "Province",
                sorted(data["Province"].unique())
            )

            d1, d2 = st.columns(2)

            with d1:
                start_date = st.date_input(
                    "Start Date",
                    value=data["Date"].min()
                )

            with d2:
                end_date = st.date_input(
                    "End Date",
                    value=data["Date"].max()
                )

            generate = st.button(
                "Generate Historical Demand"
            )

            if generate:

                province_data = data[
                    data["Province"] == province
                ]

                with st.container(border=True):

                    st.subheader("Forecast Summary")

                    m1, m2, m3 = st.columns(3)

                    m1.metric(
                        "Average Demand",
                        f"{province_data['ProvincialDemand'].mean():.0f} MW"
                    )

                    m2.metric(
                        "Peak Demand",
                        f"{province_data['ProvincialDemand'].max():.0f} MW"
                    )

                    m3.metric(
                        "Minimum Demand",
                        f"{province_data['ProvincialDemand'].min():.0f} MW"
                    )

                with st.container(border=True):

                    st.subheader("Demand Analysis")

                    c1, c2 = st.columns(2)

                    with c1:

                        fig = px.line(
                            province_data,
                            x="Date",
                            y="ProvincialDemand",
                            title="Demand Trend",
                            template=chart_theme
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    with c2:

                        weather_fig = px.line(
                            province_data,
                            x="Date",
                            y="ProvincialDemand",
                            title="Weather Placeholder",
                            template=chart_theme
                        )

                        st.plotly_chart(
                            weather_fig,
                            use_container_width=True
                        )

                with st.container(border=True):

                    st.subheader("Historical Data")

                    st.dataframe(
                        province_data,
                        use_container_width=True
                    )

        # ======================================

        else:

            st.write(
                "Select your province and forecast range."
            )

            province = st.selectbox(
                "Province",
                sorted(data["Province"].unique())
            )

            horizon = st.selectbox(
                "Forecast Days",
                [1, 2, 3, 4, 5, 6, 7]
            )

            generate = st.button(
                "Generate Forecast"
            )

            if generate:

                province_data = data[
                    data["Province"] == province
                ]

                st.metric(
                    "Forecasted Demand",
                    f"{province_data['ProvincialDemand'].mean():.0f} MW"
                )

# ==================================================
# POSTAL PAGE
# ==================================================

elif st.session_state.page == "postal":

    if st.button("← Return Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown(
        "<h1 style='text-align:center;'>Postal Code Demand</h1>",
        unsafe_allow_html=True
    )

    mode = st.radio(
        "",
        ["Historical Demand", "Forecast Demand"],
        horizontal=True,
        key="postal_mode"
    )

    with st.container(border=True):

        if mode == "Historical Demand":

            st.write(
                "Select your postal code and date range."
            )

            postal = st.selectbox(
                "Postal Code",
                sorted(data["PostalCode"].unique())
            )

            generate = st.button(
                "Generate Historical Demand",
                key="postal_hist"
            )

            if generate:

                postal_data = data[
                    data["PostalCode"] == postal
                ]

                m1, m2, m3 = st.columns(3)

                m1.metric(
                    "Average Demand",
                    f"{postal_data['PostalCodeDemand'].mean():.0f} MW"
                )

                m2.metric(
                    "Peak Demand",
                    f"{postal_data['PostalCodeDemand'].max():.0f} MW"
                )

                m3.metric(
                    "Minimum Demand",
                    f"{postal_data['PostalCodeDemand'].min():.0f} MW"
                )

                fig = px.line(
                    postal_data,
                    x="Date",
                    y="PostalCodeDemand",
                    template=chart_theme
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.dataframe(
                    postal_data,
                    use_container_width=True
                )

        else:

            postal = st.selectbox(
                "Postal Code",
                sorted(data["PostalCode"].unique())
            )

            horizon = st.selectbox(
                "Forecast Days",
                [1, 2, 3, 4, 5, 6, 7]
            )

            generate = st.button(
                "Generate Forecast",
                key="postal_forecast"
            )

            if generate:

                postal_data = data[
                    data["PostalCode"] == postal
                ]

                st.metric(
                    "Forecast Demand",
                    f"{postal_data['PostalCodeDemand'].mean():.0f} MW"
                )
