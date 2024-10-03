import requests
import pandas as pd
import os
import threading
import time
from datetime import datetime, timedelta
import websocket

def get_kline_data(pair, interval, start_time):
    try:
        params = {'pair': pair, 'interval': interval, 'limit': 10000, 'startTime': start_time}
        headers = {'Content-Type': 'application/json'}
        kline_url = "https://api.pi42.com/v1/market/klines"
        response = requests.post(kline_url, json=params, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        print(f'Kline data for {interval} fetched successfully.')
        return response_data  # Return the fetched data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err.response.status_code}: {err.response.text}")
        return None  # Return None on error
    except ValueError:
        print("Invalid JSON response received.")
        return None  # Return None on JSON error
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None  # Return None on unexpected error

def on_message(ws, message):
    print(f"Received: {message}")

def connect_websocket():
    websocket_url = "wss://api.pi42.com/v1/market/ws"
    ws = websocket.WebSocketApp(websocket_url, on_message=on_message)
    ws.run_forever()

def save_to_csv(df, filename):
    """Save DataFrame to CSV in the 'raw' directory."""
    folder_path = '.data/raw'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)  # Create the folder if it doesn't exist

    full_path = os.path.join(folder_path, filename)
    if df is not None and not df.empty:
        df.to_csv(full_path, mode='a', header=not os.path.exists(full_path), index=False)  # Append mode
        print(f"Data saved to {full_path}.")
    else:
        print(f"No data to save for {full_path}.")

def main():
    pair = "BTCINR"
    intervals = {
          "5m": 7,    # 5 minutes interval for the last 7 days
          "15m": 30,  # 15 minutes interval for the last 30 days
          "30m": 60,  # 30 minutes interval for the last 60 days
          "1h": 60,   # 1 hour interval for the last 60 days
          "6h": 60,   # 6 hours interval for the last 60 days
          "12h": 60   # 12 hours interval for the last 60 days
      }

    # Set the start time for fetching data (last X days)
    start_time_ms = int((datetime.now() - timedelta(days=60)).timestamp() * 1000)  # Change as needed

    # Dynamically fetch data for all intervals and store in DataFrames
    for interval, days in intervals.items():
          print(f"Fetching {interval} data...")
          kline_data = get_kline_data(pair, interval, start_time_ms)

          if kline_data is not None:
              df = pd.DataFrame(kline_data)
              save_to_csv(df, f"{pair}_{interval}_data.csv")  # Save to CSV
          else:
              print(f"No data fetched for interval {interval}.")

    # Start WebSocket connection in a separate thread
    print("Connecting to WebSocket...")
    ws_thread = threading.Thread(target=connect_websocket)
    ws_thread.start()

if __name__ == "__main__":
      main()