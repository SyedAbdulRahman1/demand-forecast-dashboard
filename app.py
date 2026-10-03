import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="Electrical Demand Dashboard",
    layout="wide"
)

# ======================================
# DARK MODE TOGGLE
# ======================================

dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3, label, p {
        color: white !important;
    }

    [data-testid="stMetricValue"] {
        color: #00FFB3;
    }
    </style>
    """, unsafe_allow_html=True)

bg_color = "#0E1117" if dark_mode else "white"
font_color = "white" if dark_mode else "black"
chart_theme = "plotly_dark" if dark_mode else "plotly_white"

# ======================================
# LOAD DATA
# ======================================

data = pd.read_csv("demand_data.csv")

# ======================================
# PAGE HEADER
# ======================================

st.title("⚡ Electrical Demand Forecast Dashboard")

st.write(
    "Provincial and Postal Code electrical demand forecasts."
)

# ======================================
# PROVINCIAL FORECAST SECTION
# ======================================

st.header("🏛 Provincial Demand Forecast")

province = st.selectbox(
    "Select Province",
    data["Province"].unique()
)

province_data = data[
    data["Province"] == province
]

province_forecast = province_data[
    "ProvincialDemand"
].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Forecast Demand",
        f"{province_forecast:.0f} MW"
    )

with col2:
    st.metric(
        "Maximum Demand",
        f"{province_data['ProvincialDemand'].max():.0f} MW"
    )

with col3:
    st.metric(
        "Average Demand",
        f"{province_data['ProvincialDemand'].mean():.0f} MW"
    )

st.subheader("Provincial Demand Trend")

province_fig = px.line(
    province_data,
    x="Date",
    y="ProvincialDemand",
    title=f"{province} Provincial Demand",
    template=chart_theme
)

province_fig.update_traces(
    line_width=4
)

province_fig.update_layout(
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
    font_color=font_color,
    title_font_size=22,
    hovermode="x unified"
)

st.plotly_chart(
    province_fig,
    use_container_width=True,
    theme=None
)

# ======================================
# POSTAL CODE FORECAST SECTION
# ======================================

st.header("📍 Postal Code Demand Forecast")

postal_code = st.selectbox(
    "Select Postal Code",
    data["PostalCode"].unique()
)

postal_data = data[
    data["PostalCode"] == postal_code
]

postal_forecast = postal_data[
    "PostalCodeDemand"
].mean()

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Forecast Demand",
        f"{postal_forecast:.0f} MW"
    )

with col5:
    st.metric(
        "Maximum Demand",
        f"{postal_data['PostalCodeDemand'].max():.0f} MW"
    )

with col6:
    st.metric(
        "Average Demand",
        f"{postal_data['PostalCodeDemand'].mean():.0f} MW"
    )

st.subheader("Postal Code Demand Trend")

postal_fig = px.line(
    postal_data,
    x="Date",
    y="PostalCodeDemand",
    title=f"{postal_code} Demand",
    template=chart_theme
)

postal_fig.update_traces(
    line_width=4
)

postal_fig.update_layout(
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
    font_color=font_color,
    title_font_size=22,
    hovermode="x unified"
)

st.plotly_chart(
    postal_fig,
    use_container_width=True,
    theme=None
)

# ======================================
# HISTORICAL DATA TABLE
# ======================================

st.header("📊 Historical Data")

st.dataframe(
    data,
    use_container_width=True
)
