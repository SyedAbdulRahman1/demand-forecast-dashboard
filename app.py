import streamlit as st
import pandas as pd

# Load Data
data = pd.read_csv("demand_data.csv")

# Simple Forecast
forecast = data["Demand"].mean()

# Dashboard
st.title("Electrical Demand Forecast Dashboard")

st.write("Historical Demand Data")
st.dataframe(data)

st.metric(
label="Demand Forecast",
value=f"{forecast:.0f} MW"
)

st.line_chart(data.set_index("Date"))