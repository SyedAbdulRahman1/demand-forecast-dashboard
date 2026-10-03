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
# DARK MODE
# ======================================

dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    h1, h2, h3, p, label {
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

data["Date"] = pd.to_datetime(data["Date"])

# ======================================
# HEADER
# ======================================

st.title("⚡ Electrical Demand Forecast Dashboard")

st.write(
    "Cloud-hosted dashboard for provincial and postal code demand forecasting."
)

# ======================================
# FILTER ROW
# ======================================

st.divider()

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    postal_code = st.selectbox(
        "Postal Code",
        sorted(data["PostalCode"].unique())
    )

with filter_col2:
    province = st.selectbox(
        "Province",
        sorted(data["Province"].unique())
    )

with filter_col3:
    selected_date = st.date_input(
        "Select Date",
        value=data["Date"].max()
    )

generate = st.button(
    "Generate Forecast",
    use_container_width=True
)

st.divider()

# ======================================
# DASHBOARD
# ======================================

if generate:

    province_data = data[
        data["Province"] == province
    ]

    postal_data = data[
        data["PostalCode"] == postal_code
    ]

    # ======================================
    # METRICS
    # ======================================

    st.header("Forecast Summary")

    m1, m2 = st.columns(2)

    with m1:

        province_forecast = province_data[
            "ProvincialDemand"
        ].mean()

        st.metric(
            "Provincial Forecast",
            f"{province_forecast:.0f} MW"
        )

    with m2:

        postal_forecast = postal_data[
            "PostalCodeDemand"
        ].mean()

        st.metric(
            "Postal Code Forecast",
            f"{postal_forecast:.0f} MW"
        )

    st.divider()

    # ======================================
    # CHARTS SIDE BY SIDE
    # ======================================

    chart1, chart2 = st.columns(2)

    with chart1:

        st.subheader("🏛 Provincial Demand Trend")

        province_fig = px.line(
            province_data,
            x="Date",
            y="ProvincialDemand",
            template=chart_theme,
            title=f"{province} Provincial Demand"
        )

        province_fig.update_layout(
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font_color=font_color,
            hovermode="x unified"
        )

        province_fig.update_traces(
            line_width=4
        )

        st.plotly_chart(
            province_fig,
            use_container_width=True,
            theme=None
        )

    with chart2:

        st.subheader("📍 Postal Code Demand Trend")

        postal_fig = px.line(
            postal_data,
            x="Date",
            y="PostalCodeDemand",
            template=chart_theme,
            title=f"{postal_code} Demand"
        )

        postal_fig.update_layout(
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
            font_color=font_color,
            hovermode="x unified"
        )

        postal_fig.update_traces(
            line_width=4
        )

        st.plotly_chart(
            postal_fig,
            use_container_width=True,
            theme=None
        )

    st.divider()

    # ======================================
    # DATA TABLE
    # ======================================

    st.header("📊 Historical Data")

    st.dataframe(
        data,
        use_container_width=True
    )
