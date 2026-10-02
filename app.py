import streamlit as st
import pandas as pd

# Load data
data = pd.read_csv("demand_data.csv")
# Page title
st.title("Electrical Demand Dashboard")

# Province selection
province = st.selectbox(
    "Select Province",
    data["Province"].unique()
)
# Filter data by province
province_data = data[data["Province"] == province]

# Postal code selection
postal_code = st.selectbox(
    "Select Postal Code",
    province_data["PostalCode"].unique()
)
# Filter data by postal code
filtered_data = province_data[
    province_data["PostalCode"] == postal_code
]
# Simple forecast (temporary)
forecast = filtered_data["Demand"].mean()

# Dashboard metrics
st.metric(
    label="Forecasted Demand",
    value=f"{forecast:.0f} MW"
)
# Show raw data
st.subheader("Historical Demand Data")
st.dataframe(filtered_data)

# Show demand chart
st.subheader("Demand Trend")
st.line_chart(
    filtered_data.set_index("Date")["Demand"]
)
