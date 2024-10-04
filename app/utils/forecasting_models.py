import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb
from statsmodels.tsa.arima.model import ARIMA
from keras.models import Sequential
from keras.layers import LSTM, Dense
#from fbprophet import Prophet


class ForecastingModels:
    def __init__(self, df):
        print(df.head())  # Check the first few rows of the DataFrame
        print(df.columns)  # List all columns in the DataFrame
        self.df = df
        self.df.set_index('startTime', inplace=True)

    def arima_forecast(self):
        model = ARIMA(self.df['close'], order=(5, 1, 0))  # Example order
        model_fit = model.fit()
        predictions = model_fit.forecast(steps=10)  # Forecast the next 10 data points

        # Plotting
        plt.figure(figsize=(10, 5))
        plt.plot(self.df['close'], label='Actual Prices', color='blue')
        plt.plot(predictions.index, predictions, label='Forecasted Prices', color='orange')
        plt.title('5-Minute Forecast using ARIMA')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

        return predictions

    def random_forest_forecast(self):
        self.df['lag_1'] = self.df['close'].shift(1)
        self.df.dropna(inplace=True)

        X = self.df[['lag_1']]
        y = self.df['close']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model training
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X_train, y_train)

        # Predictions
        predictions = model.predict(X_test)

        # Plotting
        plt.figure(figsize=(10, 5))
        plt.plot(y_test.index, y_test, label='Actual Prices', color='blue')
        plt.plot(y_test.index, predictions, label='Predicted Prices', color='orange')
        plt.title('15-Minute Forecast using Random Forest')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

        return predictions

    def gradient_boosting_forecast(self):
        self.df['lag_1'] = self.df['close'].shift(1)
        self.df['lag_2'] = self.df['close'].shift(2)
        self.df.dropna(inplace=True)

        X = self.df[['lag_1', 'lag_2']]
        y = self.df['close']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model training
        model = GradientBoostingRegressor(n_estimators=100)
        model.fit(X_train, y_train)

        # Predictions
        predictions = model.predict(X_test)

        # Plotting
        plt.figure(figsize=(10, 5))
        plt.plot(y_test.index, y_test, label='Actual Prices', color='blue')
        plt.plot(y_test.index, predictions, label='Predicted Prices', color='orange')
        plt.title('30-Minute Forecast using Gradient Boosting')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

        return predictions

    def lstm_forecast(self):
        data = self.df['close'].values.reshape(-1, 1)

        # Normalize the data
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)

        # Prepare training data
        x_train = []
        y_train = []
        for i in range(60, len(scaled_data)):
            x_train.append(scaled_data[i - 60:i, 0])
            y_train.append(scaled_data[i, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        # Reshape for LSTM
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Model training
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(units=1))  # Output layer
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, epochs=50, batch_size=32)

        # Prepare for predictions
        x_test = scaled_data[-60:]
        x_test = np.reshape(x_test, (1, x_test.shape[0], 1))

        # Make predictions
        predicted_price = model.predict(x_test)
        predicted_price = scaler.inverse_transform(predicted_price)  # Inverse transformation

        # Plotting
        plt.figure(figsize=(10, 5))
        plt.plot(self.df['close'], label='Actual Prices', color='blue')
        plt.axvline(x=self.df.index[-1], color='red', linestyle='--')
        plt.plot(self.df.index[-1] + pd.DateOffset(minutes=1), predicted_price[0][0], label='Predicted Price',
                 color='orange', marker='o')
        plt.title('1-Hour Forecast using LSTM')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

        return predicted_price

    # def prophet_forecast(self):
    #     # Prepare the data for Prophet
    #     df_prophet = self.df.reset_index().rename(columns={'timestamp': 'ds', 'close': 'y'})
    #
    #     # Model training
    #     model = Prophet()
    #     model.fit(df_prophet)
    #
    #     # Future dataframe for predictions
    #     future = model.make_future_dataframe(periods=6, freq='H')  # 6 hours into the future
    #     forecast = model.predict(future)
    #
    #     # Plotting
    #     fig = model.plot(forecast)
    #     plt.title('6-Hour Forecast using Prophet')
    #     plt.xlabel('Time')
    #     plt.ylabel('Price')
    #     plt.show()
    #
    #     return forecast

    def xgboost_forecast(self):
        self.df['lag_1'] = self.df['close'].shift(1)
        self.df['lag_2'] = self.df['close'].shift(2)
        self.df.dropna(inplace=True)

        X = self.df[['lag_1', 'lag_2']]
        y = self.df['close']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model training
        model = xgb.XGBRegressor(n_estimators=100)
        model.fit(X_train, y_train)

        # Predictions
        predictions = model.predict(X_test)

        # Plotting
        plt.figure(figsize=(10, 5))
        plt.plot(y_test.index, y_test, label='Actual Prices', color='blue')
        plt.plot(y_test.index, predictions, label='Predicted Prices', color='orange')
        plt.title('12-Hour Forecast using XGBoost')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

        return predictions
