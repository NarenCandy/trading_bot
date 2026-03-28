from bot.client import BinanceClient

def place_order(client, symbol, side, order_type, quantity, price=None, stop_price=None):
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
    }

    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    #if order_type.upper() == "STOP":
     #   params["type"] = "STOP_MARKET"
        #params["price"] = price
      #  params["stopPrice"] = stop_price
        #params["timeInForce"] = "GTC"

    response = client.place_order(**params)
    return response