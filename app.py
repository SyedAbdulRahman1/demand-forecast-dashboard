import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Electrical Demand Forecast Dashboard",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ==================================================
# DARK MODE TOGGLE
# ==================================================

dark_mode = st.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)

st.session_state.dark_mode = dark_mode

# ==================================================
# DARK MODE SETTINGS
# ==================================================

bg_color = "#050B18" if dark_mode else "white"
font_color = "white" if dark_mode else "black"
chart_theme = "plotly_dark" if dark_mode else "plotly_white"

if dark_mode:
    st.markdown("""
    <style>
    .stApp{
        background-color:#050B18;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

/* -------------------- */
/* TABS */
/* -------------------- */

.stTabs [role="tablist"]{
    justify-content:center;
    gap:80px;
}

.stTabs [role="tab"]{
    font-size:24px;
    font-weight:600;
    height:70px;
    padding-left:35px;
    padding-right:35px;
}

/* -------------------- */
/* RADIO BUTTONS */
/* -------------------- */

div[role="radiogroup"]{
    display:flex;
    justify-content:center;
    gap:50px;
}

/* -------------------- */
/* BUTTONS */
/* -------------------- */

.stButton{
    text-align:center;
}

.stButton button{
    background-color:#4CAF50;
    color:white;
    font-weight:bold;
    border-radius:10px;
    height:50px;
}

/* -------------------- */
/* METRICS */
/* -------------------- */

[data-testid="stMetricValue"]{
    font-size:32px;
}

/* -------------------- */
/* FIX DROPDOWN COLORS */
/* -------------------- */

.stSelectbox div[data-baseweb="select"]{
    color:black !important;
}

.stDateInput input{
    color:black !important;
}

/* -------------------- */
/* INFO SECTIONS */
/* -------------------- */

.center-text{
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

data = pd.read_csv("demand_data.csv")

data["Date"] = pd.to_datetime(
    data["Date"],
    format="%Y-%m"
)

# ==================================================
# HEADER
# ==================================================

st.markdown(
"""
<h1 style='text-align:center;
           font-size:64px;'>
Electrical Demand Forecast Dashboard
</h1>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div style='text-align:center;
            font-size:20px;
            line-height:1.8;'>

Welcome to the Canadian Electrical Demand Dashboard

<br>

Please select Provincial Demand
or Postal Code Demand to begin forecasting.

<br><br>

Cloud-hosted dashboard for provincial and postal code demand forecasting.

</div>
""",
unsafe_allow_html=True
)

st.divider()

# ==================================================
# MAIN TABS
# ==================================================

prov_tab, postal_tab = st.tabs(
    ["🏛 Provincial Demand", "📮 Postal Code Demand"]
)

# ==================================================
# PROVINCIAL TAB
# ==================================================

with prov_tab:

    st.markdown(
    """
    <h2 style='text-align:center;'>
    Canadian Provinces
    </h2>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <div style='text-align:center; font-size:18px;'>

    Choose to generate Historical Demand
    or Forecast Demand

    </div>
    """,
    unsafe_allow_html=True
    )

    mode = st.radio(
        "",
        ["Historical Demand", "Forecast Demand"],
        horizontal=True
    )

    # =====================================
    # HISTORICAL
    # =====================================

    if mode == "Historical Demand":

        st.markdown(
        """
        <div style='text-align:center;
                    font-size:18px;
                    margin-bottom:20px;'>

        Select your province and date range
        to generate historical demand.

        </div>
        """,
        unsafe_allow_html=True
        )

        left, center, right = st.columns([1,2,1])

        with center:

            province = st.selectbox(
                "Province",
                sorted(data["Province"].unique())
            )

            c1, c2 = st.columns(2)

            with c1:
                start_date = st.date_input(
                    "Start Date",
                    value=data["Date"].min()
                )

            with c2:
                end_date = st.date_input(
                    "End Date",
                    value=data["Date"].max()
                )

        col1, col2, col3 = st.columns([2,1,2])

        with col2:
            generate = st.button(
                "Generate Historical Demand",
                use_container_width=True
            )

        if generate:

            province_data = data[
                data["Province"] == province
            ]

            st.divider()

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

            chart1, chart2 = st.columns(2)

            with chart1:

                fig = px.line(
                    province_data,
                    x="Date",
                    y="ProvincialDemand",
                    title=f"{province} Demand Trend",
                    template=chart_theme
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with chart2:

                weather = px.line(
                    province_data,
                    x="Date",
                    y="ProvincialDemand",
                    title="Weather Trend (Placeholder)",
                    template=chart_theme
                )

                st.plotly_chart(
                    weather,
                    use_container_width=True
                )

            st.subheader("Historical Data")

            st.dataframe(
                province_data,
                use_container_width=True
            )

    # =====================================
    # FORECAST
    # =====================================

    else:

        st.markdown(
        """
        <div style='text-align:center;
                    font-size:18px;
                    margin-bottom:20px;'>

        Select your province and forecast range
        (1-7 days ahead) to generate demand.

        </div>
        """,
        unsafe_allow_html=True
        )

        left, center, right = st.columns([1,2,1])

        with center:

            province = st.selectbox(
                "Province",
                sorted(data["Province"].unique()),
                key="prov_forecast"
            )

            forecast_days = st.selectbox(
                "Forecast Range (Days)",
                [1,2,3,4,5,6,7]
            )

        col1, col2, col3 = st.columns([2,1,2])

        with col2:
            generate = st.button(
                "Generate Forecast",
                use_container_width=True
            )

        if generate:

            province_data = data[
                data["Province"] == province
            ]

            st.subheader("Forecast Summary")

            st.metric(
                "Forecast Demand",
                f"{province_data['ProvincialDemand'].mean():.0f} MW"
            )

# ==================================================
# POSTAL TAB
# ==================================================

with postal_tab:

    st.markdown(
    """
    <h2 style='text-align:center;'>
    Postal Code Demand
    </h2>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <div style='text-align:center;
                font-size:18px;'>

    Choose to generate Historical Demand
    or Forecast Demand

    </div>
    """,
    unsafe_allow_html=True
    )

    postal_mode = st.radio(
        "",
        ["Historical Demand", "Forecast Demand"],
        horizontal=True,
        key="postal_mode"
    )

    if postal_mode == "Historical Demand":

        st.markdown(
        """
        <div style='text-align:center;
                    font-size:18px;'>

        Select your postal code and date range
        to generate historical demand.

        </div>
        """,
        unsafe_allow_html=True
        )

        left, center, right = st.columns([1,2,1])

        with center:

            postal = st.selectbox(
                "Postal Code",
                sorted(data["PostalCode"].unique())
            )

        col1, col2, col3 = st.columns([2,1,2])

        with col2:

            generate = st.button(
                "Generate Historical Demand",
                key="postal_hist",
                use_container_width=True
            )

        if generate:

            postal_data = data[
                data["PostalCode"] == postal
            ]

            st.metric(
                "Average Postal Demand",
                f"{postal_data['PostalCodeDemand'].mean():.0f} MW"
            )

            fig = px.line(
                postal_data,
                x="Date",
                y="PostalCodeDemand",
                title=f"{postal} Demand Trend",
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

        st.markdown(
        """
        <div style='text-align:center;
                    font-size:18px;'>

        Select your postal code and forecast range
        (1-7 days ahead) to generate demand.

        </div>
        """,
        unsafe_allow_html=True
        )

        left, center, right = st.columns([1,2,1])

        with center:

            postal = st.selectbox(
                "Postal Code",
                sorted(data["PostalCode"].unique()),
                key="postal_forecast"
            )

            forecast_days = st.selectbox(
                "Forecast Range",
                [1,2,3,4,5,6,7],
                key="postal_days"
            )

        col1, col2, col3 = st.columns([2,1,2])

        with col2:

            generate = st.button(
                "Generate Forecast",
                key="postal_generate",
                use_container_width=True
            )

        if generate:

            postal_data = data[
                data["PostalCode"] == postal
            ]

            st.metric(
                "Forecast Demand",
                f"{postal_data['PostalCodeDemand'].mean():.0f} MW"
            )

            fig = px.line(
                postal_data,
                x="Date",
                y="PostalCodeDemand",
                title=f"{postal} Forecast",
                template=chart_theme
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
