import math
import streamlit as st
from scipy.stats import norm
import numpy as np
import yfinance as yf

def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        return None
    
def calc_hist_vol(ticker, period):
    data = yf.download(ticker, period=period)['Close']
    log_returns = np.log(data / data.shift(1)).dropna()
    hist_vol = log_returns.std() * np.sqrt(252)  # Annualise
    return hist_vol.iloc[0]

@st.cache_data
def get_risk_free_rate():
    try:
        risk_free_data = yf.Ticker('^IRX').history(period="1d")
        if not risk_free_data.empty and 'Close' in risk_free_data.columns:
            return risk_free_data['Close'].iloc[-1] / 100
        else:
            return 0.02
    except Exception as e:
        print(f"获取无风险利率时出错: {e}")
        return 0.02