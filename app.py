import streamlit as st
import pandas as pd

data = pd.read_csv("demand_data.csv")

province = st.selectbox(
    "Select Province",
    data["Province"].unique()
)

filtered = data[data["Province"] == province]

forecast = filtered["Demand"].mean()

st.title("Electrical Demand Dashboard")

st.metric(
    "Forecasted Demand",
    f"{forecast:.0f} MW"
)

st.line_chart(
    filtered.set_index("Date")["Demand"]
)
