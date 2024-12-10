# BSPricer: Option Pricing Web App

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-blue)](https://bspricer.streamlit.app/)

BSPricer is a lightweight web app for calculating European option prices using the Black-Scholes model. Built with Streamlit, it provides an easy-to-use interface for quickly estimating option prices.

## Try the App

👉 [Launch BSPricer](https://bspricer.streamlit.app/)

## Features

- **Real-time Mode**: Auto-fill certain parameters (i.e. spot price, volitility) with yfinance data.
- **Sandbox Mode**: Manual control of all parameters input.

## Run Locally

1. Clone the repo:
    ```bash
    git clone https://github.com/ziancn/pet-proj-BS-pricer.git
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Start the app:
    ```bash
    streamlit run app.py
    ```
