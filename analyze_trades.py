import pandas as pd
import numpy as np

# Load the CSV
df = pd.read_csv('trading_record.csv')

# Convert time to datetime
df['Time'] = pd.to_datetime(df['Time'])

# Basic Stats
total_fills = len(df)
symbols = df['Symbol'].unique()
actions = df['Action'].value_counts()

# Simple PnL Calculation Logic (Simplified for first pass)
# BOT = Buy, SLD = Sell. MNQ point value = $2 per full point.
buy_vol = df[df['Action'] == 'BOT']['Quantity'].sum()
sell_vol = df[df['Action'] == 'SLD']['Quantity'].sum()

print(f"Analysis for Beer:")
print(f"- Total Fills: {total_fills}")
print(f"- Symbols Traded: {list(symbols)}")
print(f"- Buy Orders: {actions.get('BOT', 0)}")
print(f"- Sell Orders: {actions.get('SLD', 0)}")

# Export a summary for the web UI
summary = {
    "total_trades": total_fills,
    "unique_symbols": list(symbols),
    "last_trade": df['Time'].max().strftime('%Y-%m-%d %H:%M:%S')
}
import json
with open('trade_summary.json', 'w') as f:
    json.dump(summary, f)
