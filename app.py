import streamlit as st
from utils.black_scholes import black_scholes  # 从utils中引入定价函数

st.title("Black-Scholes Option Pricer")

# User Input
S = st.number_input("Stock Price (S)", value=100.0)
K = st.number_input("Strike Price (K)", value=100.0)
T = st.number_input("Time to Maturity (T in years)", value=1.0)
r = st.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.number_input("Volatility (σ)", value=0.2)
option_type = st.selectbox("Option Type", ["call", "put"])

# Calculate
if st.button("Calculate Option Price"):
    price = black_scholes(S, K, T, r, sigma, option_type)
    st.write(f"The {option_type} option price is: ${price:.2f}")
