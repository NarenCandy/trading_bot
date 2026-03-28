from flask import Flask, request, jsonify, render_template_string
import os
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import validate
from bot.logging_config import setup_logging

load_dotenv()
setup_logging()

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Trading Bot</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono&display=swap" rel="stylesheet"/>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    min-height: 100vh; background: #0d0f14; color: #e2e8f0;
    font-family: 'Space Grotesk', sans-serif;
    display: flex; align-items: center; justify-content: center; padding: 20px;
    background-image: radial-gradient(ellipse at 20% 50%, rgba(240,185,11,0.05) 0%, transparent 60%),
                      radial-gradient(ellipse at 80% 20%, rgba(0,200,150,0.05) 0%, transparent 50%);
  }
  .card { background: #13161e; border: 1px solid #1e2433; border-radius: 16px; padding: 36px; width: 100%; max-width: 460px; box-shadow: 0 25px 60px rgba(0,0,0,0.5); }
  .header { display: flex; align-items: center; gap: 12px; margin-bottom: 28px; }
  .logo { width: 38px; height: 38px; background: linear-gradient(135deg, #f0b90b, #e8a500); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
  .header-text h1 { font-size: 1.1rem; font-weight: 700; }
  .header-text p { font-size: 0.72rem; color: #4a5568; font-family: 'Space Mono', monospace; margin-top: 2px; }
  .badge { margin-left: auto; background: rgba(0,200,150,0.1); color: #00c896; border: 1px solid rgba(0,200,150,0.2); padding: 4px 10px; border-radius: 20px; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.05em; }
  .field { margin-bottom: 16px; }
  label { display: block; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #4a5568; margin-bottom: 6px; }
  input, select { width: 100%; background: #0d0f14; border: 1px solid #1e2433; color: #e2e8f0; font-family: 'Space Mono', monospace; font-size: 0.9rem; padding: 11px 14px; border-radius: 8px; outline: none; transition: border-color 0.2s, box-shadow 0.2s; appearance: none; }
  input:focus, select:focus { border-color: #f0b90b; box-shadow: 0 0 0 3px rgba(240,185,11,0.1); }
  .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .toggle-wrap { display: grid; grid-template-columns: 1fr 1fr; border-radius: 8px; overflow: hidden; border: 1px solid #1e2433; }
  .toggle-wrap input { display: none; }
  .toggle-wrap label { padding: 11px; text-align: center; cursor: pointer; font-size: 0.82rem; font-weight: 600; color: #4a5568; margin: 0; transition: all 0.2s; background: #0d0f14; text-transform: uppercase; }
  #buy:checked ~ label[for="buy"] { background: rgba(0,200,150,0.15); color: #00c896; }
  #sell:checked ~ label[for="sell"] { background: rgba(246,70,93,0.15); color: #f6465d; }
  #price-field { display: none; }
  #price-field.show { display: block; }
  .divider { border: none; border-top: 1px solid #1e2433; margin: 20px 0; }
  .btn { width: 100%; padding: 13px; background: linear-gradient(135deg, #f0b90b, #e8a500); color: #000; font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.95rem; border: none; border-radius: 8px; cursor: pointer; transition: opacity 0.15s, transform 0.1s; }
  .btn:hover { opacity: 0.92; }
  .btn:active { transform: scale(0.98); }
  .btn:disabled { opacity: 0.4; cursor: not-allowed; }
  .result { display: none; margin-top: 20px; padding: 16px; border-radius: 10px; font-family: 'Space Mono', monospace; font-size: 0.78rem; line-height: 2; border: 1px solid #1e2433; background: #0d0f14; }
  .result.success { border-color: rgba(0,200,150,0.3); }
  .result.error { border-color: rgba(246,70,93,0.3); }
  .result-title { font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 10px; }
  .result.success .result-title { color: #00c896; }
  .result.error .result-title { color: #f6465d; }
  .kv { display: flex; justify-content: space-between; border-bottom: 1px solid #1a1d26; padding: 3px 0; }
  .kv:last-child { border: none; }
  .k { color: #4a5568; } .v { color: #e2e8f0; font-weight: 500; }
  .v.green { color: #00c896; } .v.yellow { color: #f0b90b; }
  .spinner { display: inline-block; width: 13px; height: 13px; border: 2px solid rgba(0,0,0,0.3); border-top-color: #000; border-radius: 50%; animation: spin 0.6s linear infinite; vertical-align: middle; margin-right: 6px; }
  @keyframes spin { to { transform: rotate(360deg); } }
  @media (max-width: 480px) { .card { padding: 24px; } .row { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div class="logo">₿</div>
    <div class="header-text"><h1>Trading Bot</h1><p>USDT-M Futures · Testnet</p></div>
    <span class="badge">● LIVE</span>
  </div>
  <div class="field">
    <label>Symbol</label>
    <input type="text" id="symbol" value="BTCUSDT" placeholder="e.g. BTCUSDT"/>
  </div>
  <div class="field">
    <label>Side</label>
    <div class="toggle-wrap">
      <input type="radio" name="side" id="buy" value="BUY" checked/>
      <label for="buy">▲ Buy</label>
      <input type="radio" name="side" id="sell" value="SELL"/>
      <label for="sell">▼ Sell</label>
    </div>
  </div>
  <div class="row">
    <div class="field">
      <label>Order Type</label>
      <select id="order_type" onchange="togglePrice()">
        <option value="MARKET">Market</option>
        <option value="LIMIT">Limit</option>
      </select>
    </div>
    <div class="field">
      <label>Quantity</label>
      <input type="number" id="quantity" placeholder="0.002" step="0.001" min="0.001"/>
    </div>
  </div>
  <div class="field" id="price-field">
    <label>Price (USDT)</label>
    <input type="number" id="price" placeholder="e.g. 50000" step="0.01"/>
  </div>
  <hr class="divider"/>
  <button class="btn" id="submitBtn" onclick="placeOrder()">Place Order</button>
  <div class="result" id="result"></div>
</div>
<script>
  function togglePrice() {
    const t = document.getElementById('order_type').value;
    document.getElementById('price-field').className = 'field' + (t === 'LIMIT' ? ' show' : '');
  }
  async function placeOrder() {
    const btn = document.getElementById('submitBtn');
    const result = document.getElementById('result');
    const symbol = document.getElementById('symbol').value.trim().toUpperCase();
    const side = document.querySelector('input[name="side"]:checked').value;
    const order_type = document.getElementById('order_type').value;
    const quantity = parseFloat(document.getElementById('quantity').value);
    const price = document.getElementById('price').value ? parseFloat(document.getElementById('price').value) : null;
    if (!symbol || isNaN(quantity)) { showError(result, 'Please fill in all required fields.'); return; }
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span>Placing...';
    try {
      const res = await fetch('/api/order', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol, side, order_type, quantity, price })
      });
      const data = await res.json();
      if (data.error) showError(result, data.error);
      else showSuccess(result, data);
    } catch(e) {
      showError(result, 'Network error: ' + e.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = 'Place Order';
    }
  }
  function showSuccess(el, d) {
    el.className = 'result success'; el.style.display = 'block';
    el.innerHTML = `<div class="result-title">✓ Order Placed</div>
      <div class="kv"><span class="k">Order ID</span><span class="v yellow">${d.orderId ?? '—'}</span></div>
      <div class="kv"><span class="k">Status</span><span class="v green">${d.status ?? '—'}</span></div>
      <div class="kv"><span class="k">Symbol</span><span class="v">${d.symbol ?? '—'}</span></div>
      <div class="kv"><span class="k">Side</span><span class="v">${d.side ?? '—'}</span></div>
      <div class="kv"><span class="k">Executed Qty</span><span class="v">${d.executedQty ?? '0'}</span></div>
      <div class="kv"><span class="k">Avg Price</span><span class="v">${d.avgPrice || d.price || 'N/A'}</span></div>`;
  }
  function showError(el, msg) {
    el.className = 'result error'; el.style.display = 'block';
    el.innerHTML = `<div class="result-title">✕ Failed</div><div class="kv"><span class="k">Reason</span><span class="v" style="color:#f6465d">${msg}</span></div>`;
  }
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/order", methods=["POST"])
def api_order():
    data = request.json
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    try:
        validate(data["symbol"], data["side"], data["order_type"], data["quantity"], data.get("price"), data.get("stop_price"))
        client = BinanceClient(api_key, api_secret)
        response = place_order(client, data["symbol"], data["side"], data["order_type"], data["quantity"], data.get("price"))
        return jsonify(response)
    except Exception as e:
        err = str(e)
        if "400" in err:
            return jsonify({"error": "Order rejected by Binance. Check quantity (min $100 value) and price."}), 400
        elif "401" in err:
            return jsonify({"error": "Invalid API keys. Check your .env file."}), 401
        elif "network" in err.lower() or "connect" in err.lower():
            return jsonify({"error": "Could not reach Binance. Check your internet connection."}), 500
        else:
            return jsonify({"error": err}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)