import streamlit as st

# 创建标题和副标题
st.title("Bloomberg-Style Option Pricer")
st.write("Replicating OVME option pricing interface")

# 创建左、右两栏布局
col1, col2 = st.columns(2)

# 左侧：基本输入
with col1:
    st.header("Option Parameters")
    stock_price = st.number_input("Stock Price (S)", value=100.0)
    strike_price = st.number_input("Strike Price (K)", value=100.0)
    maturity = st.slider("Time to Maturity (T, in years)", 0.1, 5.0, 1.0)
    risk_free_rate = st.number_input("Risk-Free Rate (r)", value=0.05)
    volatility = st.number_input("Volatility (σ)", value=0.2)
    option_type = st.selectbox("Option Type", ["call", "put"])

# 右侧：计算结果显示
with col2:
    st.header("Calculated Option Price")
    # Example calculation (using a placeholder function)
    # result = black_scholes(stock_price, strike_price, maturity, risk_free_rate, volatility, option_type)
    result = 12.34  # 假设的期权价格
    st.write(f"The {option_type} option price is: ${result:.2f}")
