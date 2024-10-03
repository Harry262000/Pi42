import os
import pandas as pd
intervals = ['5m', '15m', '30m', '1h', '6h', '12h']
dataframes = {}
# Path relative to the script's location
file_path = os.path.join(os.path.dirname(__file__), 'data', 'raw', f'BTCINR_{intervals}_data.csv')

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    print(f"File not found: {file_path}")
