# 📊 Stock Tracker App - Feature Roadmap & Vision

## 🎯 Objective
A smart, customizable stock portfolio tracker that automates LTP monitoring, calculates real-time profit/loss, and helps users make timely decisions with configurable thresholds and future AI enhancements.

---

## ✅ Core Features (Phase 1)

1. **Stock Tracking by LTP**
   - Periodic scraping or API-based fetching of stock prices
   - Real-time calculation of total value, profit/loss, and percentage change

2. **Stop-loss Checker & Alerts**
   - Define loss thresholds per stock
   - Visual/audio alerts or notifications when breached

3. **User-based Login System**
   - Secure user authentication
   - Per-user stock portfolio management

---

## 🔧 Extended Features (Phase 2)

4. **Demat & Broker Info (Optional)**
   - Store broker name, demat account info (read-only)
   - Optional tagging for insights like "broker A performs better"

5. **Buy/Sell Stock Threshold Configuration**
   - Set price-based triggers for each stock
   - Alert user when LTP crosses these thresholds

6. **Store Historical Stock Data (if available)**
   - Integrate with public APIs (Yahoo Finance, Nepali Stock APIs, etc.)
   - Show charts (line, candlestick, volume trend)

---

## 🤖 Advanced AI-Driven Features (Phase 3)

7. **Enable AI-based Features**
   - News sentiment analysis to predict stock impact
   - Pattern detection in historical data
   - Predictive "suggested action" (e.g., hold/sell alert)

8. **Telegram Alerts (API)**
   - Real-time alert delivery through Telegram bots
   - Configurable per-user alert preferences

9. **Portfolio Tracker Dashboard**
   - Visual portfolio with profit/loss summaries
   - Filtering by sector, performance, or alert status

---

## 🧱 Suggested Tech Stack

- **Backend:** Python + FastAPI (or Flask)
- **Frontend:** Streamlit (initial) or React + TailwindCSS
- **Database:** SQLite (start) → PostgreSQL
- **Scraping/API:** Selenium → Move to real APIs
- **Authentication:** Flask-Login / Firebase
- **AI Module (optional):** scikit-learn, pandas, Prophet (for trends)

---

## 🚀 Future Ideas

- Export portfolio snapshots to Excel
- Multi-user dashboard view
- Telegram/Email alert bots
- Mobile app (Flutter/PWA)

---

