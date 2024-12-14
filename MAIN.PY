import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import datetime

# Title of the Dashboard
st.title("Live Stock Dashboard")

# Sidebar: Stock Symbol Input and Date Range Selection
st.sidebar.header("User Input")

def user_input_features():
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, MSFT, GOOGL):", 'AAPL')
    start_date = st.sidebar.date_input("Start Date", datetime.date(2023, 1, 1))
    end_date = st.sidebar.date_input("End Date", datetime.date.today())
    return stock_symbol, start_date, end_date

# Fetch user input
symbol, start, end = user_input_features()

# Function to Load Stock Data
def load_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        return stock_data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Fetch data based on user input
stock_data = load_stock_data(symbol, start, end)

# Display Stock Data
def display_data(data, symbol):
    if data is not None and not data.empty:
        st.subheader(f"Stock Data for {symbol}")
        st.write(data.tail())
        return True
    else:
        st.error("No data available. Please check the symbol or date range.")
        return False

if display_data(stock_data, symbol):
    # Line Chart for Stock Prices
    st.subheader("Closing Price Chart")
    fig_close = go.Figure()
    fig_close.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name='Close'))
    fig_close.update_layout(title=f"Closing Prices for {symbol}", xaxis_title='Date', yaxis_title='Price (USD)')
    st.plotly_chart(fig_close)

    # Volume Chart
    st.subheader("Volume Chart")
    fig_volume = go.Figure()
    fig_volume.add_trace(go.Bar(x=stock_data.index, y=stock_data['Volume'], name='Volume'))
    fig_volume.update_layout(title=f"Trading Volume for {symbol}", xaxis_title='Date', yaxis_title='Volume')
    st.plotly_chart(fig_volume)

    # Summary Statistics
    st.subheader("Summary Statistics")
    st.write(stock_data.describe())

# Display Current Price (Live)
st.sidebar.header("Live Stock Price")
def fetch_live_price(ticker):
    try:
        live_stock = yf.Ticker(ticker)
        price = live_stock.history(period='1d')['Close'].iloc[-1]
        return round(price, 2)
    except:
        return None

current_price = fetch_live_price(symbol)
if current_price:
    st.sidebar.success(f"Current Price of {symbol}: ${current_price}")
else:
    st.sidebar.error("Unable to fetch live stock price.")

