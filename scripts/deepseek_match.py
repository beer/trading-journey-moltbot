import csv
import json

# DeepSeek refined matching logic
def solve_pnl():
    fills = []
    with open('trading_record.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fills.append(row)
    
    fills.sort(key=lambda x: x['Time'])
    
    inventory = 0
    pnl_log = []
    total_realized = 0
    multiplier = 2.0 # MNQ
    
    # We use a more aggressive matching for MNQ scalping
    active_trades = [] # Queue for FIFO matching
    
    for f in fills:
        p = float(f['Price'])
        q = int(f['Quantity'])
        side = 1 if f['Action'] == 'BOT' else -1
        
        # Check if this fill closes an existing position
        if inventory != 0 and (side * inventory < 0):
            # Closing logic
            while q > 0 and len(active_trades) > 0:
                match_p, match_q = active_trades[0]
                close_q = min(q, match_q)
                
                # Real PnL logic
                trade_pnl = (p - match_p) * close_q * multiplier * (-side)
                total_realized += trade_pnl
                
                q -= close_q
                active_trades[0] = (match_p, match_q - close_q)
                if active_trades[0][1] == 0:
                    active_trades.pop(0)
            
            if q > 0: # Switched to other side
                inventory = side * q
                active_trades.append((p, q))
            else:
                inventory += side * int(f['Quantity'])
        else:
            # Opening logic
            inventory += side * q
            active_trades.append((p, q))
            
        pnl_log.append({"t": f['Time'], "v": round(total_realized, 2)})
        
    return pnl_log

final_data = solve_pnl()
with open('data.js', 'w') as f:
    f.write(f"const tradeData = {json.dumps(final_data)};")

print(f"DeepSeek algorithm processed. Final realized: ${final_data[-1]['v']}")
