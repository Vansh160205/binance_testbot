"""
Simplified Binance Spot Testnet Trading Bot with Lightweight UI
- Uses Binance Spot Testnet base URL: https://testnet.binance.vision
- Supports MARKET, LIMIT, and OCO (One Cancels the Other) orders
- CLI and Tkinter GUI interface
- Logging for requests/responses/errors
- Loads API keys securely from .env

NOTE: This script talks to Binance SPOT Testnet. Make sure your API key/secret are from https://testnet.binance.vision.
"""

import argparse
import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from binance.client import Client
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox


class BasicBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        if testnet:
            self.client.API_URL = "https://testnet.binance.vision/api"

        # Setup logging
        self.logger = logging.getLogger("BasicBot")
        self.logger.setLevel(logging.DEBUG)
        logdir = os.path.join(os.getcwd(), "logs")
        os.makedirs(logdir, exist_ok=True)
        fh = RotatingFileHandler(os.path.join(logdir, "bot.log"), maxBytes=1_000_000, backupCount=3)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        fh.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(fh)

    def place_market_order(self, symbol: str, side: str, quantity: float):
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            self.logger.info(f"Market order: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing market order: {e}")
            raise

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float):
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_LIMIT,
                timeInForce=Client.TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )
            self.logger.info(f"Limit order: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing limit order: {e}")
            raise

    def place_oco_order(self, symbol: str, side: str, quantity: float, price: float, stop_price: float, stop_limit_price: float):
        try:
            order = self.client.create_oco_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                stopLimitPrice=stop_limit_price,
                stopLimitTimeInForce=Client.TIME_IN_FORCE_GTC
            )
            self.logger.info(f"OCO order: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing OCO order: {e}")
            raise


# ---------------- CLI ----------------
def parse_args():
    parser = argparse.ArgumentParser(description="Simplified Binance Spot Testnet Trading Bot")
    parser.add_argument("--symbol", help="Trading symbol, e.g., BTCUSDT")
    parser.add_argument("--side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", choices=["MARKET", "LIMIT", "OCO"], help="Order type")
    parser.add_argument("--quantity", type=float, help="Quantity")
    parser.add_argument("--price", type=float, help="Price for LIMIT or OCO")
    parser.add_argument("--stop-price", type=float, dest="stop_price", help="Stop price for OCO")
    parser.add_argument("--stop-limit-price", type=float, dest="stop_limit_price", help="Stop-limit price for OCO")
    parser.add_argument("--gui", action="store_true", help="Launch lightweight GUI")
    return parser.parse_args()


# ---------------- GUI ----------------
def launch_gui(bot: BasicBot):
    def place_order():
        symbol = symbol_entry.get().upper()
        side = side_var.get()
        otype = type_var.get()
        qty = float(qty_entry.get())
        try:
            if otype == "MARKET":
                resp = bot.place_market_order(symbol, side, qty)
            elif otype == "LIMIT":
                price = float(price_entry.get())
                resp = bot.place_limit_order(symbol, side, qty, price)
            elif otype == "OCO":
                price = float(price_entry.get())
                stop_price = float(stop_price_entry.get())
                stop_limit_price = float(stop_limit_price_entry.get())
                resp = bot.place_oco_order(symbol, side, qty, price, stop_price, stop_limit_price)
            else:
                messagebox.showerror("Error", "Unsupported order type")
                return

            messagebox.showinfo("Order Placed", json.dumps(resp, indent=2))
        except Exception as e:
            messagebox.showerror("Order Failed", str(e))

    root = tk.Tk()
    root.title("Trading Bot UI (Binance Spot Testnet)")

    tk.Label(root, text="Symbol").grid(row=0, column=0)
    symbol_entry = tk.Entry(root)
    symbol_entry.insert(0, "BTCUSDT")
    symbol_entry.grid(row=0, column=1)

    tk.Label(root, text="Side").grid(row=1, column=0)
    side_var = tk.StringVar(value="BUY")
    tk.OptionMenu(root, side_var, "BUY", "SELL").grid(row=1, column=1)

    tk.Label(root, text="Type").grid(row=2, column=0)
    type_var = tk.StringVar(value="MARKET")
    tk.OptionMenu(root, type_var, "MARKET", "LIMIT", "OCO").grid(row=2, column=1)

    tk.Label(root, text="Quantity").grid(row=3, column=0)
    qty_entry = tk.Entry(root)
    qty_entry.insert(0, "0.01")
    qty_entry.grid(row=3, column=1)

    tk.Label(root, text="Price (for LIMIT/OCO)").grid(row=4, column=0)
    price_entry = tk.Entry(root)
    price_entry.grid(row=4, column=1)

    tk.Label(root, text="Stop Price (OCO)").grid(row=5, column=0)
    stop_price_entry = tk.Entry(root)
    stop_price_entry.grid(row=5, column=1)

    tk.Label(root, text="Stop-Limit Price (OCO)").grid(row=6, column=0)
    stop_limit_price_entry = tk.Entry(root)
    stop_limit_price_entry.grid(row=6, column=1)

    tk.Button(root, text="Place Order", command=place_order).grid(row=7, column=0, columnspan=2, pady=10)

    root.mainloop()


# ---------------- MAIN ----------------
def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    if not api_key or not api_secret:
        print("Missing API_KEY or API_SECRET in environment. Create a .env file with API_KEY and API_SECRET.")
        sys.exit(1)

    args = parse_args()
    bot = BasicBot(api_key, api_secret, testnet=True)
        # Get account balances
    account_info = bot.client.get_account()

    # Print all balances
    for balance in account_info['balances']:
        asset = balance['asset']
        free = balance['free']
        locked = balance['locked']
        print(f"{asset}: Free={free}, Locked={locked}")

    if args.gui:
        launch_gui(bot)
        return

    try:
        if args.type == "MARKET":
            resp = bot.place_market_order(args.symbol, args.side, args.quantity)
        elif args.type == "LIMIT":
            if not args.price:
                print("LIMIT orders require --price")
                sys.exit(1)
            resp = bot.place_limit_order(args.symbol, args.side, args.quantity, args.price)
        elif args.type == "OCO":
            if not (args.price and args.stop_price and args.stop_limit_price):
                print("OCO orders require --price, --stop-price, and --stop-limit-price")
                sys.exit(1)
            resp = bot.place_oco_order(args.symbol, args.side, args.quantity, args.price, args.stop_price, args.stop_limit_price)
        else:
            print("Unsupported order type")
            sys.exit(1)

        print("Order response:\n")
        print(json.dumps(resp, indent=2))

    except Exception as e:
        print(f"Order failed: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()