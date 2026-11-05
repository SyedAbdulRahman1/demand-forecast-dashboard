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

if "generated" not in st.session_state:
    st.session_state.generated = False

# ==================================================
# DARK MODE
# ==================================================

dark_mode = st.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)

st.session_state.dark_mode = dark_mode

if dark_mode:
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    h1,h2,h3,h4,p,label {
        color:white !important;
    }

    [data-testid="stMetricValue"] {
        color:#00FFB3;
    }
    </style>
    """, unsafe_allow_html=True)

bg_color = "#0E1117" if dark_mode else "white"
font_color = "white" if dark_mode else "black"
chart_theme = "plotly_dark" if dark_mode else "plotly_white"

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
    <h1 style='text-align:center;'>
    Electrical Demand Forecast Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align:center;">
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

    st.subheader("Canadian Provinces")

    mode = st.radio(
        "Choose Option",
        ["Historical Demand", "Forecast Demand"],
        horizontal=True
    )

    # ==========================================
    # HISTORICAL DEMAND PAGE
    # ==========================================

    if mode == "Historical Demand":

        c1, c2, c3 = st.columns(3)

        with c1:
            province = st.selectbox(
                "Province",
                sorted(data["Province"].unique())
            )

        with c2:
            start_date = st.date_input(
                "Start Date",
                value=data["Date"].min()
            )

        with c3:
            end_date = st.date_input(
                "End Date",
                value=data["Date"].max()
            )

        if st.button(
            "Generate Historical Demand",
            key="prov_hist"
        ):
            st.session_state.generated = True

        if st.session_state.generated:

            province_data = data[
                (data["Province"] == province)
            ]

            st.divider()

            st.subheader("Forecast Summary")

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "Average Demand",
                    f"{province_data['ProvincialDemand'].mean():.0f} MW"
                )

            with m2:
                st.metric(
                    "Peak Demand",
                    f"{province_data['ProvincialDemand'].max():.0f} MW"
                )

            with m3:
                st.metric(
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

                fig.update_layout(
                    paper_bgcolor=bg_color,
                    plot_bgcolor=bg_color,
                    font_color=font_color
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with chart2:

                weather_placeholder = px.line(
                    province_data,
                    x="Date",
                    y="ProvincialDemand",
                    title="Weather Trend (Placeholder)",
                    template=chart_theme
                )

                weather_placeholder.update_layout(
                    paper_bgcolor=bg_color,
                    plot_bgcolor=bg_color,
                    font_color=font_color
                )

                st.plotly_chart(
                    weather_placeholder,
                    use_container_width=True
                )

            st.subheader("Historical Data")

            st.dataframe(
                province_data,
                use_container_width=True
            )

    # ==========================================
    # FORECAST PAGE
    # ==========================================

    else:

        c1, c2 = st.columns(2)

        with c1:

            province = st.selectbox(
                "Province",
                sorted(data["Province"].unique()),
                key="forecast_province"
            )

        with c2:

            forecast_days = st.selectbox(
                "Forecast Range (Days)",
                [1, 2, 3, 4, 5, 6, 7]
            )

        if st.button(
            "Generate Forecast",
            key="prov_forecast"
        ):

            province_data = data[
                data["Province"] == province
            ]

            st.subheader("Forecast Summary")

            st.metric(
                "Forecasted Demand",
                f"{province_data['ProvincialDemand'].mean():.0f} MW"
            )

            chart1, chart2 = st.columns(2)

            with chart1:

                fig = px.line(
                    province_data,
                    x="Date",
                    y="ProvincialDemand",
                    title="Forecast Trend",
                    template=chart_theme
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with chart2:

                weather_fig = px.line(
                    province_data,
                    x="Date",
                    y="ProvincialDemand",
                    title="Weather Forecast Placeholder",
                    template=chart_theme
                )

                st.plotly_chart(
                    weather_fig,
                    use_container_width=True
                )

# ==================================================
# POSTAL CODE TAB
# ==================================================

with postal_tab:

    st.subheader("Postal Code Demand")

    mode = st.radio(
        "Choose Option",
        ["Historical Demand", "Forecast Demand"],
        horizontal=True,
        key="postal_mode"
    )

    # ==========================================
    # POSTAL HISTORICAL
    # ==========================================

    if mode == "Historical Demand":

        c1, c2, c3 = st.columns(3)

        with c1:

            postal = st.selectbox(
                "Postal Code",
                sorted(data["PostalCode"].unique())
            )

        with c2:

            start_date = st.date_input(
                "Start Date",
                value=data["Date"].min(),
                key="postal_start"
            )

        with c3:

            end_date = st.date_input(
                "End Date",
                value=data["Date"].max(),
                key="postal_end"
            )

        if st.button(
            "Generate Historical Demand",
            key="postal_hist"
        ):

            postal_data = data[
                data["PostalCode"] == postal
            ]

            st.subheader("Postal Demand Summary")

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "Average Demand",
                    f"{postal_data['PostalCodeDemand'].mean():.0f} MW"
                )

            with m2:
                st.metric(
                    "Peak Demand",
                    f"{postal_data['PostalCodeDemand'].max():.0f} MW"
                )

            with m3:
                st.metric(
                    "Minimum Demand",
                    f"{postal_data['PostalCodeDemand'].min():.0f} MW"
                )

            col1, col2 = st.columns(2)

            with col1:

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

            with col2:

                weather_fig = px.line(
                    postal_data,
                    x="Date",
                    y="PostalCodeDemand",
                    title="Weather Trend Placeholder",
                    template=chart_theme
                )

                st.plotly_chart(
                    weather_fig,
                    use_container_width=True
                )

            st.dataframe(
                postal_data,
                use_container_width=True
            )

    # ==========================================
    # POSTAL FORECAST
    # ==========================================

    else:

        c1, c2 = st.columns(2)

        with c1:

            postal = st.selectbox(
                "Postal Code",
                sorted(data["PostalCode"].unique()),
                key="postal_forecast_code"
            )

        with c2:

            forecast_days = st.selectbox(
                "Forecast Range",
                [1,2,3,4,5,6,7],
                key="postal_days"
            )

        if st.button(
            "Generate Forecast",
            key="postal_forecast"
        ):

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
                title="Forecast Trend",
                template=chart_theme
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
