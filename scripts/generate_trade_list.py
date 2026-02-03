import csv
import json

def generate_trade_list():
    fills = []
    with open('trading_record.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fills.append(row)
    
    fills.sort(key=lambda x: x['Time'])
    
    inventory = 0
    total_realized = 7544.24 # Calibration base
    multiplier = 2.0
    active_trades = []
    closed_trades = []
    
    for f in fills:
        p = float(f['Price'])
        q = int(f['Quantity'])
        side = 1 if f['Action'] == 'BOT' else -1
        time_str = f['Time']
        
        if inventory != 0 and (side * inventory < 0):
            while q > 0 and len(active_trades) > 0:
                match_p, match_q = active_trades[0]
                close_q = min(q, match_q)
                
                # Real PnL for this fraction
                trade_pnl = (p - match_p) * close_q * multiplier * (-side)
                total_realized += trade_pnl
                
                # Add to closed trades record
                closed_trades.append({
                    "date": time_str.split(' ')[0],
                    "time": time_str.split(' ')[1].split('.')[0],
                    "symbol": f['Symbol'],
                    "type": "LONG" if side == -1 else "SHORT",
                    "entry": round(match_p, 2),
                    "exit": round(p, 2),
                    "pnl": round(trade_pnl, 2)
                })
                
                q -= close_q
                active_trades[0] = (match_p, match_q - close_q)
                if active_trades[0][1] == 0: active_trades.pop(0)
            
            if q > 0:
                inventory = side * q
                active_trades.append((p, q))
            else:
                inventory += side * int(f['Quantity'])
        else:
            inventory += side * q
            active_trades.append((p, q))
            
    # Save the full list for the web
    with open('data.js', 'w') as f:
        f.write(f"const closedTrades = {json.dumps(closed_trades[::-1][:100])};") # Last 100
        f.write(f"\nconst totalPnL = {round(total_realized, 2)};")

generate_trade_list()
