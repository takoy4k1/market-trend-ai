from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model_serve import predict_forecast
import pandas as pd
from config import FEATURES_DATA_PATH

app = FastAPI(title="Market Trend AI API")

# Allow Streamlit dashboard to talk to this API
app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Endpoint 1: Health check ──────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}

# ── Endpoint 2: Get forecast ──────────────────────────────
@app.get("/forecast")
def forecast(days: int = 30):
    try:
        predictions = predict_forecast(days)
        return {"status": "ok", "days": days, "forecast": predictions}
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

# ── Endpoint 3: Get historical data ──────────────────────
@app.get("/history")
def history(days: int = 90):
    try:
        df = pd.read_csv(FEATURES_DATA_PATH)
        df = df.tail(days)

        # FIX: remove NaN values
        df = df.fillna(0)

        return {"status": "ok", "history": df.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))