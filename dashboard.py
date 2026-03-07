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
st.cache_data.clear() if refresh else None

@st.cache_data(ttl=3600)  # cache for 1 hour
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

    # Forecast line (dashed)
    if forecast is not None:
        fig.add_trace(go.Scatter(
            x=forecast["date"], y=forecast["predicted_price"],
            name="AI Forecast",
            line=dict(color="#3dffa0", width=2, dash="dash")
        ))
        # Confidence band
        fig.add_trace(go.Scatter(
            x=forecast["date"].tolist() + forecast["date"].tolist()[::-1],
            y=forecast["upper"].tolist() + forecast["lower"].tolist()[::-1],
            fill="toself", fillcolor="rgba(61,255,160,0.08)",
            line=dict(color="rgba(255,255,255,0)"),
            name="Confidence Range", showlegend=True
        ))

    fig.update_layout(title="Price History + AI Forecast",
                      xaxis_title="Date", yaxis_title="Price ($)",
                      height=450, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# ── AI INSIGHTS (from Person B's insight_engine.py) ───────
st.subheader("🤖 AI-Generated Insights")
try:
    from scripts.insight_engine import generate_insight
    insight = generate_insight(history, forecast)
    st.info(f"💡 {insight}")
except ImportError:
    st.info("💡 Insight engine not connected yet — will appear here once Person B's insight_engine.py is ready")
except Exception as e:
    st.info(f"💡 Error generating insight: {str(e)}")

# ── ANOMALY ALERTS (from Person B's anomaly.py) ──────────
st.subheader("🚨 Anomaly Alerts")
try:
    from scripts.anomaly import detect_anomalies
    anomalies = detect_anomalies(history)
    if len(anomalies) > 0:
        for _, row in anomalies.iterrows():
            st.warning(f"⚠️ Unusual activity on {row['date']}: price was ${row['close_price']:.2f}")
    else:
        st.success("✅ No anomalies detected in the selected period")
except:
    st.warning("Anomaly module not connected yet")