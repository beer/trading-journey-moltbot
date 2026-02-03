---
name: trading-web-master
description: 專門用於管理 Beer 的 Trading Journey 網站 (crazy-money.online)。包含自動化 UI 同步、交易數據精確解析、以及 GitHub 自動化部署。當需要更新網頁佈局、處理新的交易 CSV 檔案、或發布新功能到網站時使用。
---

# Trading Web Master

此技能確保 Crazy Money 網站的數據精確度與 UI 一致性。

## 核心流程

### 1. UI 同步 (Sidepanel & Navigation)
每當修改 `index.html` 的側邊欄或導覽列時，必須執行同步腳本，確保其餘頁面 (`battle-station.html`, `project-management.html`, `reports.html`) 同步更新。
- 使用工具：`python3 scripts/sync_ui.py`

### 2. 數據自動化處理
當用戶傳送新的交易紀錄 CSV 時：
1. 將檔案存為 `trading_record.csv`。
2. 執行 `python3 scripts/process_trades.py`。
3. 此腳本會根據 MNQ ($2/pt) 規格，精確還原 PnL 並更新 `data.js`。

### 3. 自動部署
完成修改後，執行 `python3 scripts/deploy_github.py`。
- 自動執行：`git add .`, `git commit`, `git push`。

## 視覺與 OCR 指南
當接收到 TradeZella 截圖時：
- 識別 Setup 名稱 (PO3, OTE, CVDS)。
- 提取已勾選的 Checklist 狀態。
- 將數據存入 `current_setup.json` 並更新 Battle Station 頁面。

## 常用指令
- `python3 scripts/sync_ui.py` - 同步全站 UI。
- `python3 scripts/deploy_github.py "Commit Message"` - 快速部署。
