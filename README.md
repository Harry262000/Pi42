# Pi42's Real-Time Cryptocurrency Trading Analysis

## Project Overview

This project involves retrieving historical Kline (candlestick) data for BTCINR from the Pi42 exchange using their API/WebSocket. The primary focus is to process the data into several distinct time frames—5 minutes, 15 minutes, 30 minutes, 1 hour, 6 hours, and 12 hours—tailoring them for different trading strategies. 

## Data Retrieval

Accessing the data through the provided API posed some challenges initially. After reviewing the documentation, I opted to utilize WebSocket for real-time data streaming. This method allowed for efficient gathering of the necessary historical Kline data for BTCINR.

## Data Processing

Once the data was successfully retrieved, I split it into several DataFrames, each optimized for specific trading strategies:

### Time Frame Breakdown

- **5-Minute DataFrame**
  - **Model Used**: Short-Term Prediction Model (e.g., ARIMA, LSTM)
  - **Data Points**: Approximately 300-500 data points
  - **Rationale**: This short time frame requires high-frequency data to capture rapid price fluctuations. A minimum of 300 data points provides a robust dataset for generating actionable insights.

- **15-Minute DataFrame**
  - **Model Used**: Short to Mid-Term Prediction Model (e.g., Random Forest, XGBoost)
  - **Data Points**: Approximately 500-700 data points
  - **Rationale**: With a slightly longer time frame, a minimum of 500 data points allows for better trend detection and reduces noise compared to 5-minute data, improving model performance.

- **30-Minute DataFrame**
  - **Model Used**: Mid-Term Prediction Model (e.g., Gradient Boosting)
  - **Data Points**: Approximately 700-1,000 data points
  - **Rationale**: This data frame balances short and long-term perspectives, requiring around 700 data points to effectively identify mid-term trends without overfitting to market noise.

- **1-Hour DataFrame**
  - **Model Used**: Long-Term Prediction Model (e.g., LSTM, SARIMA)
  - **Data Points**: Approximately 1,000-2,000 data points
  - **Rationale**: An hour's data provides a broader view of market dynamics. A dataset of 1,000 points allows for capturing significant patterns and trends while maintaining predictive power.

- **6-Hour DataFrame**
  - **Model Used**: Long-Term Forecasting Model (e.g., LSTM, Prophet)
  - **Data Points**: Approximately 2,000-3,000 data points
  - **Rationale**: Longer time frames reduce the impact of short-term volatility. Around 2,000 data points are necessary to establish reliable long-term trends and insights.

- **12-Hour DataFrame**
  - **Model Used**: Long-Term Strategic Model (e.g., XGBoost)
  - **Data Points**: Approximately 3,000+ data points
  - **Rationale**: This time frame is ideal for swing trading. A larger dataset of 3,000 points ensures the model can capture significant price movements and macro trends, providing robust predictions.

## Analysis and Model Development

With the data structured according to the specified time frames, I conducted exploratory data analysis to uncover trends and patterns. Key technical indicators, such as Moving Averages and the Relative Strength Index (RSI), were calculated to enhance the predictive capabilities of the models.

Despite significant efforts in developing a predictive model to forecast future price movements, I encountered challenges in achieving satisfactory accuracy with the predictions. This aspect of the project remains a work in progress and is under continuous improvement.

## Visualization

The findings and insights from this analysis are summarized using relevant graphs and charts created with Matplotlib. These visualizations highlight the performance of the models and the effectiveness of the trading strategies derived from the processed data.

## Conclusion

This project serves as a foundational exploration of cryptocurrency trading strategies using real-time data. The insights and models developed here provide a starting point for further research and refinement in cryptocurrency trading methodologies.
