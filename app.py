import streamlit as st
import pandas as pd
import joblib

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="✈️ Monthly Flight Delay Predictor",
    page_icon="✈️",
    layout="wide",
)

# ── Load Dropdown Options from Dataset ───────────────────────────────────────
@st.cache_data
def load_options():
    df = pd.read_csv("airline_delay.csv")
    carriers = sorted(df["carrier"].dropna().unique().tolist())
    airports = sorted(df["airport"].dropna().unique().tolist())
    return carriers, airports

carrier_options, airport_options = load_options()

# ── Load Model & Preprocessor ─────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    preprocessor = joblib.load("flight_preprocessor.pkl")
    model = joblib.load("flight_rf_model.pkl")
    return preprocessor, model

preprocessor, model = load_artifacts()

# ── Header ────────────────────────────────────────────────────────────────────
st.title("✈️ Monthly Flight Delay Predictor")
st.markdown(
    """
    This app predicts the **total aggregated delay minutes** for a specific airline at a specific
    airport over an entire month — **not** the delay of a single individual flight.
    Enter the parameters below and click **Predict Total Delay** to get the forecast.
    """
)
st.divider()

# ── Input Form ────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    year = st.number_input(
        "📅 Year",
        min_value=2010,
        max_value=2030,
        value=2024,
        step=1,
        help="The year for the prediction.",
    )
    month = st.slider(
        "📆 Month",
        min_value=1,
        max_value=12,
        value=6,
        help="The month (1 = January, 12 = December).",
    )

with col2:
    carrier = st.selectbox(
        "🏷️ Carrier Code",
        options=carrier_options,
        index=carrier_options.index("DL") if "DL" in carrier_options else 0,
        help="Select the airline IATA carrier code.",
    )

with col3:
    airport = st.selectbox(
        "🏢 Airport Code",
        options=airport_options,
        index=airport_options.index("ATL") if "ATL" in airport_options else 0,
        help="Select the airport IATA code.",
    )

    arr_flights = st.number_input(
        "🛬 Arriving Flights (arr_flights)",
        min_value=1,
        value=500,
        step=10,
        help="Total number of arriving flights for that airline/airport/month.",
    )

st.divider()

# ── Prediction ────────────────────────────────────────────────────────────────
predict_btn = st.button("🔮 Predict Total Delay", type="primary", use_container_width=True)

if predict_btn:
    if not carrier:
        st.error("⚠️ Please enter a valid Carrier code.")
    elif not airport:
        st.error("⚠️ Please enter a valid Airport code.")
    else:
        input_df = pd.DataFrame(
            [[year, month, carrier, airport, arr_flights]],
            columns=["year", "month", "carrier", "airport", "arr_flights"],
        )

        with st.spinner("Running inference…"):
            try:
                X_transformed = preprocessor.transform(input_df)
                prediction = model.predict(X_transformed)[0]

                st.success("✅ Prediction complete!")

                res_col1, res_col2 = st.columns([1, 2])
                with res_col1:
                    st.metric(
                        label="🕐 Predicted Total Delay",
                        value=f"{prediction:,.2f} minutes",
                    )
                with res_col2:
                    hours = prediction / 60
                    st.metric(
                        label="⏱️ Equivalent Hours",
                        value=f"{hours:,.1f} hours",
                    )

                st.info(
                    "ℹ️ **Note:** This is the **combined total delay** of all arriving flights for "
                    f"carrier **{carrier}** at airport **{airport}** for "
                    f"month **{month}/{year}** — not the delay of any single flight."
                )

            except ValueError as ve:
                st.error(
                    f"⚠️ **Prediction failed — unseen category encountered.**\n\n"
                    f"The preprocessor could not handle one of your inputs "
                    f"(carrier `{carrier}` or airport `{airport}` may not exist in the training data).\n\n"
                    f"**Details:** `{ve}`"
                )
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: `{e}`")

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Powered by a Random Forest model trained on historical FAA airline on-time performance data.")
