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
        df = pd.read_csv(f"BTCINR_{interval}_data.csv")  # D:\Github\Pi42\data
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
        eda = EDA(data_dict, selected_interval)  

        # Basic statistics
        st.subheader("Basic Statistics")
        st.write(eda.df.describe()) 

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
   # Provide a dropdown for model selection, which includes time frames
    models = [
        "ARIMA (5-Minute Forecast)",
        "Random Forest (15-Minute Forecast)",
        "Gradient Boosting (30-Minute Forecast)",
        "LSTM (1-Hour Forecast)",
        "Prophet (6-Hour Forecast)",
        "XGBoost (12-Hour Forecast)"
    ]

    selected_model = st.selectbox("Select Forecasting Model", models)

    data_dict = load_data()

    df = data_dict[selected_model.split(' ')[-2]]  

    forecaster = ForecastingModels(df)

    # Button to run the forecast
    if st.button("Run Forecast"):
        with st.spinner("Running the model, please wait..."):
            if selected_model == "ARIMA (5-Minute Forecast)":
                predictions = forecaster.arima_forecast()
            elif selected_model == "Random Forest (15-Minute Forecast)":
                predictions = forecaster.random_forest_forecast()
            elif selected_model == "Gradient Boosting (30-Minute Forecast)":
                predictions = forecaster.gradient_boosting_forecast()
            elif selected_model == "LSTM (1-Hour Forecast)":
                predictions = forecaster.lstm_forecast()
            elif selected_model == "Prophet (6-Hour Forecast)":
                predictions = forecaster.prophet_forecast()
            elif selected_model == "XGBoost (12-Hour Forecast)":
                predictions = forecaster.xgboost_forecast()

            # Display the predictions as a table
            st.subheader("Current Predictions")
            st.write(predictions)

            # Plot the predictions
            plt.figure(figsize=(10, 5))
            plt.plot(predictions.index, predictions['close'], label='Predicted Prices', color='blue')
            plt.title(f'{selected_model} Predictions')
            plt.xlabel('Time')
            plt.ylabel('Price')
            plt.legend()
            st.pyplot(plt)
# Backtesting Page
elif page == "Backtesting":
    st.header("Backtesting")
    # Backtesting details...
