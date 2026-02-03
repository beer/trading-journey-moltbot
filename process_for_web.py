import csv
from datetime import datetime

trades = []
with open('trading_record.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        trades.append(row)

# Calculate Daily PnL (Simplified estimate for UI)
# In reality, we need to match BOT/SLD, but for a quick visual curve:
daily_pnl = {}
for t in trades:
    date = t['Time'].split(' ')[0]
    # Price is in index 8, Action in index 6
    price = float(t['Price'])
    qty = int(t['Quantity'])
    if date not in daily_pnl: daily_pnl[date] = 0
    
    # Very rough estimate for visualization: 
    # Long-term PnL trend follows price action vs fixed baseline
    if t['Action'] == 'BOT': daily_pnl[date] -= (price * qty * 0.01) # Nominal cost
    else: daily_pnl[date] += (price * qty * 0.01)

# Generate JS data
js_content = f"const tradeData = {daily_pnl};"
with open('data.js', 'w') as f:
    f.write(js_content)

print(f"Processed {len(trades)} trades and generated data.js")
