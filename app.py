import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from utils import black_scholes, calc_hist_vol

# Page configuration
st.set_page_config(
    page_title='Naïve Option Pricer',
    page_icon='🧸',
    layout='wide')
#  Zian Chen LinkedIn link
profile_url = 'https://www.linkedin.com/in/zian-zayn-chen'
icon_url = 'https://cdn-icons-png.flaticon.com/512/174/174857.png'
st.sidebar.markdown(f'<a href="{profile_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="{icon_url}" width="16" height="16" style="vertical-align: middle; margin-right: 10px;">`Zian (Zayn) Chen`</a>', unsafe_allow_html=True)

# SIDEBAR #
st.sidebar.title('Naïve Option Pricer')

use_live_data = st.sidebar.checkbox('Use live data', value=True)

ticker = st.sidebar.text_input('Underlying Ticker', value='AAPL')

if use_live_data:
    stock = yf.Ticker(ticker)
    last_px = stock.info['currentPrice']
    risk_free_rate = yf.Ticker('^IRX').history(period="1d")['Close'][-1] / 100

spot_px = st.sidebar.number_input('Spot Price', value=last_px if use_live_data else 100)

# Strike Price
k_col1, k_col2 = st.sidebar.columns([2,3])
with k_col1:
    strike_input_method = st.selectbox('Strike', ('Price', 'Percent'))
with k_col2:
    if strike_input_method == 'Price':
        strike_px = st.number_input('Strike Price', value=spot_px)
    else:
        strike_pct = st.number_input('% of Spot', value=100.0)
        strike_px = (spot_px * strike_pct) / 100

# Maturity
t = st.sidebar.number_input('Time to maturity (Years)', value=1.0)

# Risk free rate
rfr = st.sidebar.number_input('Risk free rate', value=risk_free_rate if use_live_data else 0.04, format="%.4f")

# Volatility
v_col1, v_col2 = st.sidebar.columns([2,3])
with v_col1:
    vol_type = st.selectbox('Vol Type', ['Hist 6mo', 'Hist 3mo', 'Hist 1mo'], disabled=False if use_live_data else True)
    period = vol_type.split()[-1]

if use_live_data and ticker:
    try:
        vol_value = calc_hist_vol(ticker, period)
    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {e}")
        vol_value = 0.2
else:
    vol_value = 0.2

with v_col2:
    vol = st.number_input('Vol', value=vol_value, disabled=True if use_live_data else False)

# Main Page

call_px = black_scholes(
    S=spot_px,
    K=strike_px,
    T=t,
    sigma=vol_value,
    r=rfr,
    option_type='call')

put_px = black_scholes(
    S=spot_px,
    K=strike_px,
    T=t,
    sigma=vol_value,
    r=rfr,
    option_type='put')

if use_live_data and ticker:
    try:
        stock_data = yf.Ticker(ticker).history(period="1y")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name="Close Price"))
        fig.update_layout(
            title=f'{ticker} - 1Y',
            template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to fetch data for {ticker}: {e}")

st.markdown(f"""
    <style>
    .card-container {{
        display: flex;
        gap: 1rem;
        withth: 100%;
        margin: 0;
    }}
    .card {{
        flex-grow: 1;               
        min-width: 150px;    
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        text-align: center;
        font-size: 1rem;
        font-weight: bold;
    }}
    .call-card {{
        background-color: #b8f1b0;
        color: #006400;
    }}
    .put-card {{
        background-color: #f1b0b0;
        color: #8b0000;
    }}
    </style>
    
    <div style="display: flex; gap: 1rem; justify-content: center;">
        <div class="card call-card">
            CALL Px<br>
            Price: ${call_px:.2f} <br>
            Price (%): {call_px/spot_px*100:.2f}%
        </div>
        <div class="card put-card">
            PUT Px<br>
            ${put_px:.2f} <br>
            Price (%): {put_px/spot_px*100:.2f}%
        </div>
    </div>
""", unsafe_allow_html=True)