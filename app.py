import base64
import io
import math
import struct
import wave
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
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

if "play_click_sound" not in st.session_state:
    st.session_state.play_click_sound = False


def trigger_click_sound():
    st.session_state.play_click_sound = True


def make_click_sound_data_uri():
    sample_rate = 22050
    frame_count = int(sample_rate * 0.06)
    audio = io.BytesIO()

    with wave.open(audio, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        for frame in range(frame_count):
            envelope = 1 - frame / frame_count
            sample = int(
                0.35
                * envelope
                * 32767
                * math.sin(2 * math.pi * 1400 * frame / sample_rate)
            )
            wav_file.writeframesraw(struct.pack("<h", sample))

    encoded_audio = base64.b64encode(audio.getvalue()).decode("ascii")
    return f"data:audio/wav;base64,{encoded_audio}"


if st.session_state.play_click_sound:
    sound_data_uri = make_click_sound_data_uri()
    components.html(
        f'<audio autoplay src="{sound_data_uri}"></audio>',
        height=0,
    )
    st.session_state.play_click_sound = False

# ==================================================
# DARK MODE
# ==================================================

dark_mode = st.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)

st.session_state.dark_mode = dark_mode

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
    height:62px;
    font-size:26px;
    font-weight:600;
    border-radius:12px;
    padding:0.35rem 0.9rem;
}

/* METRICS */

[data-testid="stMetricValue"]{
    font-size:34px;
}

/* TAB/TEXT SIZE */

.stTabs [role="tab"] {
    font-size:18px;
    font-weight:600;
}

div[role="radiogroup"]{
    display:flex;
    justify-content:center;
    gap:50px;
    font-size:16px;
}

/* ACCENT BUTTONS */

.stButton button{
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    color:white;
    font-weight:bold;
    border: none;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
}

.stButton button:hover {
    background: linear-gradient(135deg, #1e40af, #2563eb);
    color:white;
}

[data-testid="stContainer"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# DATA
# ==================================================

DATA_PATH = Path(__file__).resolve().parent / "demand_data.csv"

if not DATA_PATH.exists():
    st.error(
        f"CSV file not found at: {DATA_PATH}. "
        "Make sure the file is in the same folder as app.py and run the app with: "
        "streamlit run app.py"
    )
    st.stop()

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    df.columns = [column.strip() for column in df.columns]
    df["Province"] = df["Province"].astype(str).str.strip()
    df["PostalCode"] = df["PostalCode"].astype(str).str.strip()
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m", errors="coerce")
    df["ProvincialDemand"] = pd.to_numeric(df["ProvincialDemand"], errors="coerce")
    df["PostalCodeDemand"] = pd.to_numeric(df["PostalCodeDemand"], errors="coerce")

    return df


data = load_data()


def show_historical_results(records, demand_column):
    if records.empty:
        st.warning("No historical data is available for the selected date range.")
        return

    st.subheader("Historical Demand Summary")
    average, peak, minimum = st.columns(3)
    demand = records[demand_column]

    average.metric("Average Demand", f"{demand.mean():.0f} MW")
    peak.metric("Peak Demand", f"{demand.max():.0f} MW")
    minimum.metric("Minimum Demand", f"{demand.min():.0f} MW")

    figure = px.line(
        records,
        x="Date",
        y=demand_column,
        title="Demand Trend",
        template=chart_theme,
    )
    st.plotly_chart(figure, use_container_width=True)
    st.dataframe(records, use_container_width=True)


def show_forecast_result(records, demand_column, horizon):
    if records.empty:
        st.warning("No data is available for the selected location.")
        return

    forecast = records.sort_values("Date")[demand_column].tail(horizon).mean()
    st.metric("Estimated Demand", f"{forecast:.0f} MW")


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
            "Provincial Demand Dashboard",
            use_container_width=True,
            on_click=trigger_click_sound,
        ):
            st.session_state.page = "provincial"
            st.rerun()

    with col2:

        if st.button(
            "Postal Code Demand Dashboard",
            use_container_width=True,
            on_click=trigger_click_sound,
        ):
            st.session_state.page = "postal"
            st.rerun()

# ==================================================
# PROVINCIAL PAGE
# ==================================================

elif st.session_state.page == "provincial":

    if st.button("← Return Home", on_click=trigger_click_sound):
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
                "Generate Historical Demand",
                on_click=trigger_click_sound,
            )

            if generate:

                province_data = data[
                    (data["Province"] == province)
                    & (data["Date"] >= pd.Timestamp(start_date))
                    & (data["Date"] <= pd.Timestamp(end_date))
                ].sort_values("Date")
                show_historical_results(province_data, "ProvincialDemand")

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
                "Generate Forecast",
                on_click=trigger_click_sound,
            )

            if generate:
                province_data = data[data["Province"] == province]
                show_forecast_result(province_data, "ProvincialDemand", horizon)

# ==================================================
# POSTAL PAGE
# ==================================================

elif st.session_state.page == "postal":

    if st.button("← Return Home", on_click=trigger_click_sound):
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
                "Generate Historical Demand",
                key="postal_hist",
                on_click=trigger_click_sound,
            )

            if generate:
                postal_data = data[
                    (data["PostalCode"] == postal)
                    & (data["Date"] >= pd.Timestamp(start_date))
                    & (data["Date"] <= pd.Timestamp(end_date))
                ].sort_values("Date")
                show_historical_results(postal_data, "PostalCodeDemand")

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
                key="postal_forecast",
                on_click=trigger_click_sound,
            )

            if generate:
                postal_data = data[data["PostalCode"] == postal]
                show_forecast_result(postal_data, "PostalCodeDemand", horizon)
