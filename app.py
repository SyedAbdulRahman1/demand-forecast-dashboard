import streamlit as st
import pandas as pd
# ======================================
# LOAD DATA
# ======================================
data = pd.read_csv("demand_data.csv")

# ======================================
# PAGE HEADER
# ======================================
st.set_page_config(
    page_title="Electrical Demand Dashboard",
    layout="wide"
)
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
province_forecast = province_data["ProvincialDemand"].mean()

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

st.line_chart(
    province_data.set_index("Date")["ProvincialDemand"]
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

postal_forecast = postal_data["PostalCodeDemand"].mean()

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

st.line_chart(
    postal_data.set_index("Date")["PostalCodeDemand"]
)

# ======================================
# DATA SECTION
# ======================================

st.header("📊 Historical Data")

st.dataframe(data)
