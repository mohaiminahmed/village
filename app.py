import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date, timedelta
from streamlit_option_menu import option_menu
import mplfinance as mpf

# Set the title and logo of the app
st.set_page_config(
    page_title="Village",
    page_icon=":rocket:",
    #layout='wide',
)

st.write("hello")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Top Options Menu
selected = option_menu(
    menu_title=None,
    options=["HOME","FINANCIAL","TECHNICAL"],
    icons=["house","bar-chart-line","heart-pulse"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!importat", "background-color": "light gray"},
        "icon": {"color": "#f8c471"},
        "nav-link": {
            "font-size": "20px",
            "text-align": "center",
            "margin": "0px",
        },
    "nav-link-selected": {"background-color": "#5f6a6a"}
    },
)

if selected == "HOME":
    # Columns for the top options
    col1, col2, col3, col4 = st.columns(4)

    # Get ticker from user
    ticker = col1.selectbox('Ticker Symbol: ', [
    'AIAD',
    'AITX',
    'BNGO',
    'CSCO',
    'CLOV',
    'DBD',
    'DNA',
    'HQGE',
    'OPEN',
    'PBR',
    'T',
    'TSLA',
    'TTCM',
    'ZIM'
    ])

    # Date picker
    default_start_date = date.today() - timedelta(days=90)
    start_date = col2.date_input('Start Date', value=default_start_date)
    end_date = col3.date_input('End Date')

    # Fetch data from Yahoo Finance
    @st.cache
    def fetch_data(ticker):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data
    data = fetch_data(ticker)

    # Using Plotly for Candlestick
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])

    # Customize the chart layout
    fig.update_layout(
        title=f"{ticker} Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price"
    )

    #Display the Candlestick Chart
    st.plotly_chart(fig)


if selected == "TECHNICAL":
    # Function to create the Renko chart
    def create_renko_chart(data):
        # Convert the data to the required format for Renko chart
        renko_data = data.copy()
        renko_data['Date'] = renko_data.index
        renko_data.set_index('Date', inplace=True)

        # Create the Renko chart using candlestick visualization
        fig, _ = mpf.plot(renko_data, type='renko', style='yahoo', show_nontrading=True, mav=(5, 10, 20), returnfig=True)

        # Display the Renko chart using Streamlit
        st.pyplot(fig)

    # Columns for the top options
    col1, col2, col3, col4 = st.columns(4)

    # Get ticker from user
    ticker = col1.selectbox('Ticker Symbol: ', [
        'AIAD',
        'AITX',
        'BNGO',
        'CSCO',
        'CLOV',
        'DBD',
        'DNA',
        'HQGE',
        'OPEN',
        'PBR',
        'T',
        'TSLA',
        'TTCM',
        'ZIM'
    ])

    # Date picker
    default_start_date = date.today() - timedelta(days=365)
    start_date = col2.date_input('Start Date', value=default_start_date)
    end_date = col3.date_input('End Date')

    # Fetch data from Yahoo Finance
    @st.cache
    def fetch_data(ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data

    data = fetch_data(ticker, start_date, end_date)

    # Create a Streamlit app
    st.write('1. Displaying Renko chart for', ticker)
    create_renko_chart(data)
