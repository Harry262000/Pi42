# Integrating Pi42 API for Crypto Forecasting - BTCINR

This project demonstrates the integration of the Pi42 API to forecast cryptocurrency prices for BTCINR. The Streamlit application enables data visualization, exploratory data analysis (EDA), and forecasting models.

## Table of Contents

1. [Project Overview](#project-overview)
2. [File Structure](#file-structure)
3. [Sections and Functionality](#sections-and-functionality)
   - [Objective](#objective)
   - [API Integration](#api-integration)
   - [Data Overview](#data-overview)
   - [Exploratory Analysis (EDA)](#exploratory-analysis-eda)
   - [Forecasting Models](#forecasting-models)
   - [Backtesting](#backtesting)
4. [Known Issues](#known-issues)
5. [Getting Started](#getting-started)
6. [Contributing](#contributing)
7. [Contact](#contact)

## Project Overview

The goal of this project is to demonstrate the ability to work with real-time cryptocurrency data from the Pi42 API, perform detailed analysis, and apply machine learning techniques to forecast price movements.

## File Structure

    ```plaintext
    .
    ├── api
    │   └── api.py                    # API integration code
    ├── data
    │   ├── BTCINR_5m_data.csv        # Data for 5-minute intervals
    │   ├── BTCINR_15m_data.csv       # Data for 15-minute intervals
    │   ├── BTCINR_30m_data.csv       # Data for 30-minute intervals
    │   ├── BTCINR_1h_data.csv        # Data for 1-hour intervals
    │   ├── BTCINR_6h_data.csv        # Data for 6-hour intervals
    │   └── BTCINR_12h_data.csv       # Data for 12-hour intervals
    ├── utils
    │   ├── content.py                # Project description and API handling
    │   ├── EDA.py                    # EDA functions
    │   ├── forecasting_models.py      # Forecasting models
    │   └── visualization.py           # Data visualization
    └── main.py                       # Streamlit app entry point

## Sections and Functionality

### Objective
**File Path**: `main.py`  
**Description**: This section outlines the project's goals, including the ability to analyze cryptocurrency data and apply machine learning techniques.

### API Integration
**File Path**: `api/api.py`  
**Description**: This section provides an overview of how the Pi42 API is integrated, including fetching live data for analysis.

### Data Overview
**File Path**: `utils/visualization.py`  
**Description**: This section loads and displays various data intervals using the `DataVisualizer` class.

### Exploratory Analysis (EDA)
**File Path**: `utils/EDA.py`  
**Description**: This section provides multiple EDA options such as price change analysis, volume analysis, and moving average analysis.

### Forecasting Models
**File Path**: `utils/forecasting_models.py`  
**Description**: This section is currently under development. Forecasting models like ARIMA, Random Forest, and LSTM will be implemented here.

### Backtesting
**File Path**: `main.py`  
**Description**: This section will outline the backtesting framework for validating forecasting models.

## Known Issues
- **Model Training**: The training of the forecasting models is still ongoing. There are challenges related to overfitting that need to be addressed.
- **Functionality**: As of now, EDA is fully functional, while the forecasting section is still being worked on.

## Getting Started
To get started with this project:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/repository.git
    ```

2. Navigate to the project directory:
    ```bash
    cd repository
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Streamlit application:
    ```bash
    streamlit run main.py
    ```

Follow the app's navigation to explore the different sections.
