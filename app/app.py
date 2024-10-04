import streamlit as st
from utils.visualization import DataVisualizer 
import logging
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils.content import Roadmap, ProjectDescription, APIHandler
from utils.EDA import EDA
from utils.forecasting_models import ForecastingModels
import time

# page config
st.set_page_config(page_title="Integrating Pi42 API for Crypto Forecasting", layout="wide")

# Main title
st.title("Integrating Pi42 API for Crypto Forecasting - BTCINR")

# Sidebar for navigation
page = st.sidebar.radio("Navigate", ["Objective", "API", "Data Overview", "Exploratory Analysis", "Forecasting", "Backtesting"])

# Load data
@st.cache_data
def load_data():
    intervals = ['5m', '15m', '30m', '1h', '6h', '12h']
    dataframes = {}

    for interval in intervals:
        df = pd.read_csv(f"/workspaces/pi42/app/BTCINR_{interval}_data.csv")  # D:\Github\Pi42\data
        df['startTime'] = pd.to_datetime(df['startTime'], unit='ms')
        df['endTime'] = pd.to_datetime(df['endTime'], unit='ms')
        df.set_index('startTime', inplace=True)
        dataframes[interval] = df
    return dataframes

# Objective
if page == "Objective":
    st.header("Objective / Goal : ")
    st.write("The goal is to demonstrate the ability to work with Pi42 API/socket data, perform data analysis, and apply machine learning techniques in a real-world trading context.")
    st.header("Project Roadmap")
    roadmap = Roadmap()
    roadmap.display_roadmap()

# Pi42 API Data Retrieval
if page == "API":
    st.title("API Integration Overview")
    project_description = ProjectDescription.get_description()
    st.markdown(project_description)
    api_file_path = "api/api.py"  
    APIHandler.display_api_code(api_file_path)

# Data Overview Page
if page == "Data Overview":
    st.header("Data Overview")
    data_dict = load_data()
    
    # instance of DataVisualizer
    visualizer = DataVisualizer(data_dict)

    # Display the selected data
    visualizer.display_selected_data()
    
    # Multi-timeframe chart
    visualizer.create_multi_timeframe_chart()

# Exploratory Analysis Page
elif page == "Exploratory Analysis":
    st.header("Exploratory Data Analysis (EDA)")
    # Load your data first
    data_dict = load_data()
    # Get the selected interval from the user
    intervals = list(data_dict.keys())
    selected_interval = st.selectbox("Select Interval", intervals)

    # Check if the selected interval is valid
    if selected_interval in data_dict:
        # Initialize EDA with both data_dict and selected_interval
        eda = EDA(data_dict, selected_interval)  # Pass both arguments

        # Basic statistics
        st.subheader("Basic Statistics")
        st.write(eda.df.describe())  # Use eda.df to display basic statistics

        # Let users select which analysis they want to perform
        st.subheader("Select EDA Options")
        eda_options = st.multiselect(
            "Select the type of analysis to perform:",
            ["Price Change Analysis", "Plot Open Prices", "Volume Over Time",
             "Moving Average Analysis", "RSI Analysis", "Seasonal Decomposition"]
        )

        # Run the selected EDA functions based on user input
        if "Price Change Analysis" in eda_options:
            st.subheader("Price Change Analysis")
            eda.price_change_analysis()

        if "Plot Open Prices" in eda_options:
            st.subheader("Open Prices Over Time")
            eda.plot_open_prices()

        if "Volume Over Time" in eda_options:
            st.subheader("Volume Over Time")
            eda.volume_over_time()

        if "Moving Average Analysis" in eda_options:
            st.subheader("Moving Average Analysis")
            eda.moving_average_analysis()

        if "RSI Analysis" in eda_options:
            st.subheader("Relative Strength Index (RSI) Analysis")
            eda.rsi_analysis()

        if "Seasonal Decomposition" in eda_options:
            st.subheader("Seasonal Decomposition")
            eda.seasonal_decomposition()
    else:
        st.warning("Please select a valid interval.")

# Forecasting Page
elif page == "Forecasting":
    st.header("Price Forecasting")
    st.write("## Forecasting Models Overview")

    # Provide a dropdown for model selection
    models = ["5-Minute Forecast (ARIMA)",
              "15-Minute Forecast (Random Forest)",
              "30-Minute Forecast (Gradient Boosting)",
              "1-Hour Forecast (LSTM)",
              "6-Hour Forecast (Prophet)",
              "12-Hour Forecast (XGBoost)"]

    selected_model = st.selectbox("Select Forecasting Model", models)

    # Load your data first
    data_dict = load_data()
    selected_interval = st.selectbox("Select Interval", list(data_dict.keys()))
    df = data_dict[selected_interval]

    # Create an instance of the ForecastingModels class
    forecaster = ForecastingModels(df)

    # Display the last run result if available
    if 'last_predictions' in st.session_state:
        st.subheader("Last Run Predictions")
        st.write(st.session_state.last_predictions)

    # Check last run time
    current_time = time.time()
    last_run_time = st.session_state.get('last_run_time', 0)
    time_diff = current_time - last_run_time

    # Button to run the forecast
    if st.button("Run Forecast"):
        if time_diff < 5:  # You can adjust this value to 10 for a longer wait
            st.warning("Please wait a few seconds before running the model again.")
        else:
            with st.spinner("Running the model, please wait..."):
                # Execute the selected forecasting model
                if selected_model == "5-Minute Forecast (ARIMA)":
                    predictions = forecaster.arima_forecast()
                elif selected_model == "15-Minute Forecast (Random Forest)":
                    predictions = forecaster.random_forest_forecast()
                elif selected_model == "30-Minute Forecast (Gradient Boosting)":
                    predictions = forecaster.gradient_boosting_forecast()
                elif selected_model == "1-Hour Forecast (LSTM)":
                    predicted_price = forecaster.lstm_forecast()
                    predictions = predicted_price  # Adjust as needed
                elif selected_model == "6-Hour Forecast (Prophet)":
                    forecast = forecaster.prophet_forecast()
                    predictions = forecast  # Adjust as needed
                elif selected_model == "12-Hour Forecast (XGBoost)":
                    predictions = forecaster.xgboost_forecast()

                # Store the last predictions and current time in session state
                st.session_state.last_predictions = predictions
                st.session_state.last_run_time = current_time

                # Display the predictions after running the model
                st.subheader("Current Predictions")
                st.write(predictions)

# Backtesting Page
elif page == "Backtesting":
    st.header("Backtesting")
    # Backtesting details...
