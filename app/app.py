import streamlit as st
from utils.visualization import DataVisualizer 
import logging
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils.content import Roadmap, ProjectDescription, APIHandler

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
    data_dict = {}

    base_url = "https://raw.githubusercontent.com/Harry262000/pi42/main/data/raw/BTCINR_"

    for interval in intervals:
        try:
            # Construct the raw GitHub URL for each interval
            url = f"{base_url}{interval}_data.csv"
            print(f"Loading data for interval: {interval} from {url}")

            # Load the CSV data
            df = pd.read_csv(url)
            df['startTime'] = pd.to_datetime(df['startTime'], unit='ms')
            df['endTime'] = pd.to_datetime(df['endTime'], unit='ms')
            df.set_index('startTime', inplace=True)
            data_dict[interval] = df
            print(f"Data for {interval} loaded successfully.")

        except Exception as e:
            print(f"Error loading data for {interval}: {e}")

    return data_dict


# def load_data():
#     intervals = ['5m', '15m', '30m', '1h', '6h', '12h']
#     dataframes = {}
#
#     for interval in intervals:
#         file_path = os.path.join("data", "raw")
#         df = pd.read_csv(f"https://raw.githubusercontent.com/Harry262000/pi42/main/data/raw/BTCINR_{intervals}_data.csv")  #D:\Github\Pi42\data
#         df['startTime'] = pd.to_datetime(df['startTime'], unit='ms')
#         df['endTime'] = pd.to_datetime(df['endTime'], unit='ms')
#         df.set_index('startTime', inplace=True)
#         dataframes[interval] = df
#     return dataframes
# def load_data():
#     intervals = ['5m', '15m', '30m', '1h', '6h', '12h']
#     dataframes = {}
    
#     for interval in intervals:
#         # Construct the file path
#         file_path = os.path.join("data", "raw", f"BTCINR_{interval}_data.csv")
        
#         try:
#             # Read the CSV file
#             df = pd.read_csv(file_path)
#             df['startTime'] = pd.to_datetime(df['startTime'], unit='ms')
#             df['endTime'] = pd.to_datetime(df['endTime'], unit='ms')
#             df.set_index('startTime', inplace=True)
#             dataframes[interval] = df
            
#         except FileNotFoundError:
#             print(f"File not found: {file_path}. Please check the file path.")
#         except pd.errors.EmptyDataError:
#             print(f"No data: {file_path} is empty.")
#         except Exception as e:
#             print(f"An error occurred while loading data for interval '{interval}': {e}")
    
#     return dataframes

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
    intervals = list(load_data().keys())
    selected_interval = st.selectbox("Select Interval", intervals)

    # Load selected interval data
    data_dict = load_data()
    df = data_dict[selected_interval]

    # Basic statistics
    st.subheader("Basic Statistics")
    st.write(df.describe())

    # Plotting price trends
    st.subheader("Price Trend")
    plt.figure(figsize=(12, 6))
    plt.plot(df['close'], label='Close Price', color='blue')
    plt.title(f'{selected_interval} Close Price Trend')
    plt.xlabel('Date')
    plt.ylabel('Price (INR)')
    plt.legend()
    st.pyplot(plt)

    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    correlation = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title("Correlation Heatmap")
    st.pyplot(plt)

    # Display distribution of prices
    st.subheader("Price Distribution")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['close'], bins=30, kde=True, color='orange')
    plt.title("Distribution of Close Prices")
    plt.xlabel("Price (INR)")
    st.pyplot(plt)

# Forecasting Page
elif page == "Forecasting":
    st.header("Price Forecasting")
    st.write("""## Forecasting (Under Development)""")
    # Implementation details...

# Backtesting Page
elif page == "Backtesting":
    st.header("Backtesting")
    # Backtesting details...
