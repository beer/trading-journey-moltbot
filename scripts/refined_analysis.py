import csv
from datetime import datetime

# Contract multiplier for MNQ
MULTIPLIER = 2.0 
COMMISSION_PER_SIDE = 0.5 # Estimated if not provided

trades_log = []
with open('trading_record.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        trades_log.append(row)

# Match BOT and SLD to form completed trades
inventory = 0
cost_basis = 0
pnl_history = []
cumulative_pnl = 0

# Sort by time
trades_log.sort(key=lambda x: x['Time'])

for t in trades_log:
    price = float(t['Price'])
    qty = int(t['Quantity'])
    action = t['Action']
    
    if action == 'BOT':
        # If we were short, we cover. If flat, we go long.
        if inventory < 0:
            # Covering part of a short
            covered_qty = min(abs(inventory), qty)
            realized = (cost_basis - price) * covered_qty * MULTIPLIER
            cumulative_pnl += realized - (covered_qty * COMMISSION_PER_SIDE * 2)
            inventory += qty
        else:
            # Adding to long
            inventory += qty
            cost_basis = (cost_basis * (inventory - qty) + price * qty) / inventory
    else: # SLD
        if inventory > 0:
            # Selling part of a long
            sold_qty = min(inventory, qty)
            realized = (price - cost_basis) * sold_qty * MULTIPLIER
            cumulative_pnl += realized - (sold_qty * COMMISSION_PER_SIDE * 2)
            inventory -= qty
        else:
            # Adding to short
            inventory -= qty
            cost_basis = (cost_basis * (abs(inventory) - qty) + price * qty) / abs(inventory)
            
    pnl_history.append({
        "time": t['Time'],
        "pnl": round(cumulative_pnl, 2)
    })

# Output JS for the web
import json
with open('data.js', 'w') as f:
    f.write(f"const tradeData = {json.dumps(pnl_history)};")

print(f"Refined PnL calculation complete. Total Cumulative PnL: ${cumulative_pnl:.2f}")
