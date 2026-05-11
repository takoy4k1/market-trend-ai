# 📈 AI Market Trend Analysis

AI Market Trend Analysis is a full-stack data science and machine learning application designed to fetch, clean, and analyze stock market data. It uses Facebook's Prophet model to forecast future prices and leverages an AI Insight Engine to provide actionable intelligence on market anomalies and trends.

## Features

* **Data Pipeline:** Automated fetching and cleaning of stock market data (powered by AlphaVantage).
* **Predictive Modeling:** Time-series forecasting using a pre-trained Prophet model to predict future stock prices.
* **FastAPI Backend:** A fast and scalable REST API that serves historical data and forecasts to the frontend.
* **Streamlit Dashboard:** An interactive and visually appealing web interface to explore price history, forecasts, and AI-generated insights.
* **Anomaly Detection & Insights:** Automatically flags unusual price movements and generates intelligent insights combining historical context and future predictions.

## Tech Stack

* **Backend:** FastAPI, Python
* **Frontend:** Streamlit, Plotly
* **Machine Learning:** Prophet, scikit-learn, Pandas
* **Data Source:** AlphaVantage API

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd market-trend-ai
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your API keys:
   ```env
   ALPHA_VANTAGE_KEY=your_alphavantage_key
   OPENAI_KEY=your_openai_key
   ```

## Running the Application

You will need to run both the FastAPI backend and the Streamlit frontend.

**1. Start the FastAPI Backend**
```bash
source venv/bin/activate
uvicorn main:app --port 8000 --reload
```

**2. Start the Streamlit Dashboard**
In a new terminal window:
```bash
source venv/bin/activate
streamlit run dashboard.py
```

The dashboard will be available at `http://localhost:8501`.

## Project Structure

* `dashboard.py`: Streamlit frontend application.
* `main.py`: FastAPI backend application.
* `data_clean.py`: Scripts for data preprocessing and missing value handling.
* `model_serve.py`: Model loading and forecasting logic.
* `config.py`: Global configuration and environment variable management.
* `scripts/`: Contains the anomaly detection algorithms, the insight engine, and model training notebooks.
* `models/`: Directory containing the pre-trained `.pkl` models.
* `data/`: Raw, cleaned, and feature-engineered CSV data files.
