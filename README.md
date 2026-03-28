# Binance Futures Testnet Trading Bot

A simple trading bot built in Python that lets you place orders on Binance Futures Testnet.
Built as part of an internship application task. No real money involved — testnet only.

---

## What it does

- Place MARKET and LIMIT orders on Binance Futures (USDT-M Testnet)
- Supports both BUY and SELL sides
- Two ways to use it — terminal (CLI) or browser (Web UI)
- Logs every request and response to a file for debugging
- Validates your input before sending anything to Binance

---

## Project Structure
```
trading_bot/
  bot/
    client.py         → handles all communication with Binance API
    orders.py         → builds and sends the actual order
    validators.py     → checks your input before anything is sent
    logging_config.py → sets up logging to file
  cli.py              → run orders from the terminal
  ui.py               → browser-based UI (Flask)
  logs/
    trading_bot.log   → all requests, responses and errors get saved here
  requirements.txt
  .env.example
```

---

## Setup

### Step 1 — Get Testnet API Keys

1. Go to [testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in with your GitHub account
3. Click the **API Key** tab
4. Hit **Generate HMAC_SHA256 Key** and copy both the API Key and Secret

### Step 2 — Clone and install
```bash
git clone https://github.com/YOUR_USERNAME/trading-bot.git
cd trading-bot

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### Step 3 — Add your API keys
```bash
cp .env.example .env
```

Open `.env` and paste your keys:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_secret_key_here
```

---

## Running the CLI

Basic format:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

**Market order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

**Limit order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 70000
```

What you'll see:
```
--- Order Request ---
Symbol     : BTCUSDT
Side       : SELL
Type       : LIMIT
Quantity   : 0.002
Price      : 70000.0
--------------------

--- Order Response ---
Order ID   : 13001986017
Status     : NEW
Symbol     : BTCUSDT
Side       : SELL
Executed   : 0.000
Avg Price  : 0.00
--------------------
✅ Order placed successfully!
```

## Running the Web UI
```bash
python ui.py
```

Open your browser and go to `http://localhost:5000`

Fill in the form, hit Place Order — done.

---

## Logging

Every order you place gets logged to `logs/trading_bot.log`:
```
[2026-03-28 16:42:14] INFO - Sending POST to /fapi/v1/order | params: ['symbol', 'side', 'type', ...]
[2026-03-28 16:42:15] INFO - Response 200: {"orderId":13001933673,"symbol":"BTCUSDT",...}
```

Errors are logged too — useful when something goes wrong with the API.

---

## Things to note

- Minimum order value on testnet is **$100** (Binance rule) — use at least 0.002 BTC
- STOP orders are not supported on Binance Futures Testnet — only MARKET and LIMIT work
- The `.env` file is in `.gitignore` — your API keys won't be pushed to GitHub
- Testnet resets occasionally so old order IDs may disappear

---

## Tech used

- Python 3.10.10
- httpx — for making HTTP requests to Binance
- Flask — for the web UI
- python-dotenv — for reading API keys from .env