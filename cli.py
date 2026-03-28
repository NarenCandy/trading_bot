import argparse
import os
from dotenv import load_dotenv

load_dotenv()

from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import validate
from bot.logging_config import setup_logging

setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", dest="order_type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, type=float, help="e.g. 0.002")
    parser.add_argument("--price", type=float, default=None, help="required for LIMIT")

    args = parser.parse_args()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("Error: API keys not found in .env file")
        return

    try:
        validate(args.symbol, args.side, args.order_type, args.quantity, args.price)

        # summary printed AFTER validation passes
        print("\n--- Order Request ---")
        print(f"Symbol     : {args.symbol.upper()}")
        print(f"Side       : {args.side.upper()}")
        print(f"Type       : {args.order_type.upper()}")
        print(f"Quantity   : {args.quantity}")
        if args.price:
            print(f"Price      : {args.price}")
        print("--------------------\n")

        client = BinanceClient(api_key, api_secret)
        response = place_order(client, args.symbol, args.side, args.order_type, args.quantity, args.price)

        print("\n--- Order Response ---")
        print(f"Order ID   : {response.get('orderId')}")
        print(f"Status     : {response.get('status')}")
        print(f"Symbol     : {response.get('symbol')}")
        print(f"Side       : {response.get('side')}")
        print(f"Executed   : {response.get('executedQty')}")
        print(f"Avg Price  : {response.get('avgPrice')}")
        print("--------------------")
        print("✅ Order placed successfully!\n")

    except ValueError as e:
        print(f"Validation Error: {e}")
        print("❌ Order failed!\n")
    except Exception as e:
        print(f"Something went wrong: {e}")
        print("❌ Order failed!\n")

if __name__ == "__main__":
    main()