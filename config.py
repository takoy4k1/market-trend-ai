import os
from dotenv import load_dotenv

load_dotenv()

# ── Market Settings ──────────────────────────────────────
SYMBOL         = "AAPL"          # stock/product to analyse
FORECAST_DAYS  = 30             # how many days ahead to predict

# ── File Paths ───────────────────────────────────────────
RAW_DATA_PATH      = f"data/raw/{SYMBOL}_raw.csv"
CLEAN_DATA_PATH    = f"data/clean/{SYMBOL}_clean.csv"
FEATURES_DATA_PATH = f"data/features/{SYMBOL}_features.csv"
MODEL_PATH         = f"models/prophet_model.pkl"

# ── API Keys ─────────────────────────────────────────────
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
OPENAI_KEY        = os.getenv("OPENAI_KEY")

# ── API Settings ─────────────────────────────────────────
FASTAPI_PORT  = 8000
ANOMALY_THRESHOLD = 2.5  # z-score above this = anomaly