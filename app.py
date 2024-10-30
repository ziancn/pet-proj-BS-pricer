# import streamlit as st

# # 创建标题和副标题
# st.title("Bloomberg-Style Option Pricer")
# st.write("Replicating OVME option pricing interface")

# # 创建左、右两栏布局
# col1, col2 = st.columns(2)

# # 左侧：基本输入
# with col1:
#     st.header("Option Parameters")
#     stock_price = st.number_input("Stock Price (S)", value=100.0)
#     strike_price = st.number_input("Strike Price (K)", value=100.0)
#     maturity = st.slider("Time to Maturity (T, in years)", 0.1, 5.0, 1.0)
#     risk_free_rate = st.number_input("Risk-Free Rate (r)", value=0.05)
#     volatility = st.number_input("Volatility (σ)", value=0.2)
#     option_type = st.selectbox("Option Type", ["call", "put"])

# # 右侧：计算结果显示
# with col2:
#     st.header("Calculated Option Price")
#     # Example calculation (using a placeholder function)
#     # result = black_scholes(stock_price, strike_price, maturity, risk_free_rate, volatility, option_type)
#     result = 12.34  # 假设的期权价格
#     st.write(f"The {option_type} option price is: ${result:.2f}")


import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils import black_scholes

# 设置应用标题
st.title("Enhanced Option Pricer with Stock Data")

# 输入股票代码
ticker = st.text_input("Enter Stock Ticker:", value="AAPL")

# 定义日期范围选择
end_date = st.date_input("End Date", value=datetime.today())
start_date = st.date_input("Start Date", value=end_date - timedelta(days=365))

# 获取数据
if ticker:
    # 使用yfinance查询股票数据
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    if not stock_data.empty:
        # 显示当前价格
        current_price = float(stock_data["Close"].iloc[-1])
        st.write(f"Current price of {ticker}: ${current_price:.2f}")

        # 绘制互动图表
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name="Close Price"))
        fig.update_layout(
            title=f"{ticker} Stock Price",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified"
        )
        
        # 显示互动图表
        st.plotly_chart(fig, use_container_width=True)

        # 其余的Black-Scholes期权计算部分可以放在这里
        st.header("Option Parameters")
        strike_price = st.number_input("Strike Price (K)", value=float(current_price))
        maturity = st.slider("Time to Maturity (T, in years)", 0.1, 5.0, 1.0)
        risk_free_rate = st.number_input("Risk-Free Rate (r)", value=0.05)
        volatility = st.number_input("Volatility (σ)", value=0.2)
        option_type = st.selectbox("Option Type", ["call", "put"])

        # Black-Scholes 计算函数（假设已经定义在其他文件中）
        result = black_scholes(current_price, strike_price, maturity, risk_free_rate, volatility, option_type)
        result = 12.34  # 示例结果
        st.write(f"The {option_type} option price is: ${result:.2f}")
    else:
        st.write("No data found for the provided ticker symbol.")
