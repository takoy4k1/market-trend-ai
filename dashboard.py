import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from config import FEATURES_DATA_PATH, FASTAPI_PORT

API_URL = f"http://localhost:{FASTAPI_PORT}"

# ── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="📈 Market Trend AI",
    layout="wide"
)
st.title("📈 AI Market Trend Analysis")

# ── SIDEBAR CONTROLS ─────────────────────────────────────
st.sidebar.header("Settings")
forecast_days = st.sidebar.slider("Forecast days ahead", 7, 60, 30)
history_days  = st.sidebar.slider("Days of history to show", 30, 365, 90)
refresh       = st.sidebar.button("🔄 Refresh Data")

# ── FETCH DATA FROM API ───────────────────────────────────
if refresh:
    st.cache_data.clear()

@st.cache_data(ttl=3600)
def get_forecast(days):
    try:
        r = requests.get(f"{API_URL}/forecast?days={days}", timeout=10)
        return pd.DataFrame(r.json()["forecast"])
    except:
        return None

def get_history(days):
    try:
        df = pd.read_csv(FEATURES_DATA_PATH)
        return df.tail(days)
    except:
        return None

history  = get_history(history_days)
forecast = get_forecast(forecast_days)

# ── METRIC CARDS ─────────────────────────────────────────
if history is not None:
    col1, col2, col3, col4 = st.columns(4)
    curr   = history["close_price"].iloc[-1]
    prev   = history["close_price"].iloc[-2]
    change = ((curr - prev) / prev) * 100
    col1.metric("Current Price",   f"${curr:.2f}", f"{change:+.2f}%")
    if forecast is not None:
        pred  = forecast["predicted_price"].iloc[-1]
        updown = "📈" if pred > curr else "📉"
        col2.metric(f"{updown} {forecast_days}d Forecast", f"${pred:.2f}")
    col3.metric("Days of Data", len(history))
    col4.metric("Forecast Period", f"{forecast_days} days")

st.divider()

# ── MAIN CHART ───────────────────────────────────────────
if history is not None:
    fig = go.Figure()

    # Historical line
    fig.add_trace(go.Scatter(
        x=history["date"], y=history["close_price"],
        name="Actual Price", line=dict(color="#4f9eff", width=2)
    ))

    # Forecast line + confidence band
    if forecast is not None:
        fig.add_trace(go.Scatter(
            x=forecast["date"], y=forecast["predicted_price"],
            name="AI Forecast",
            line=dict(color="#3dffa0", width=2, dash="dash")
        ))

        # Support both "upper"/"lower" and "upper_bound"/"lower_bound" column names
        upper_col = "upper" if "upper" in forecast.columns else "upper_bound"
        lower_col = "lower" if "lower" in forecast.columns else "lower_bound"

        if upper_col in forecast.columns and lower_col in forecast.columns:
            fig.add_trace(go.Scatter(
                x=forecast["date"].tolist() + forecast["date"].tolist()[::-1],
                y=forecast[upper_col].tolist() + forecast[lower_col].tolist()[::-1],
                fill="toself", fillcolor="rgba(61,255,160,0.08)",
                line=dict(color="rgba(255,255,255,0)"),
                name="Confidence Range", showlegend=True
            ))

    fig.update_layout(title="Price History + AI Forecast",
                      xaxis_title="Date", yaxis_title="Price ($)",
                      height=450, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# ── AI INSIGHTS & ANOMALIES ──────────────────────────────
st.subheader("🤖 AI-Generated Insights")

# Detect anomalies ONCE, outside any try block
anomalies = []
try:
    from scripts.anomaly import detect_anomalies
    if history is not None:
        anomaly_df = detect_anomalies(history)
        anomalies = anomaly_df.to_dict(orient='records')
except Exception as e:
    st.warning(f"Anomaly detection error: {str(e)}")

# Generate insight
try:
    from scripts.insight_engine import generate_insight

    if forecast is not None:
        insight = generate_insight(
            history,
            forecast.to_dict("records"),
            anomalies
        )
        st.info("💡 " + insight)
    else:
        st.info("💡 Forecast data not available yet.")

except ImportError:
    st.info("💡 Insight engine not connected yet")
except Exception as e:
    st.warning(f"Insight engine error: {str(e)}")


# ── ANOMALY ALERTS ───────────────────────────────────────
st.subheader("🚨 Anomaly Alerts")

if len(anomalies) > 0:
    for a in anomalies:
        st.warning(
            f"⚠️ {a['date']} — Price ${a['close_price']} ({a['deviation_pct']}% deviation)"
        )
else:
    st.success("✅ No anomalies detected")