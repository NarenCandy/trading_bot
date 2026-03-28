def validate(symbol, side, order_type, quantity, price=None, stop_price=None):
    if not symbol or not symbol.strip():
        raise ValueError("Symbol is required")
    if not symbol.strip().isalpha():
        raise ValueError("Symbol should only contain letters e.g. BTCUSDT")
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0")
    if order_type.upper() == "LIMIT" and not price:
        raise ValueError("Price is required for LIMIT orders")