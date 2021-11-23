import sys
import time
from statistics import mean

import ccxt
from ccxt.base import errors as err

import config
import load
from custom_input import *

kraken = load.get_exchange()

oid = my_input("Order ID?")
o = kraken.fetch_order(oid)

while True:
    factor = my_input("Trailing factor? (e.g. 0.9 for a 10% drop)")
    factor = float(factor)
    if factor > 0 and factor < 1:
        break

while o["status"] == "open":
    print("Iterate")
    # fetch 3 prices, take average. Smoothes out a bit
    ob = kraken.fetch_order_book(o["symbol"], 3)
    bids = ob['bids']
    avg_price = mean([bid[0] for bid in bids])
    sp = round(avg_price * factor, 2)

    if o["price"] < sp:
        print(f"Update order to new sell price {sp} in 3 seconds")
        time.sleep(3)
        o = kraken.fetch_order(o["id"])
        if o["status"] == "open":
            kraken.cancel_order(o["id"])
            o = kraken.create_order(o["symbol"], "stop-loss", "sell", o["amount"], sp, { "leverage":"5" } )
        else:
            print(f"Order executed or filled in the meantime: o['status']")
            sys.exit()
    time.sleep(15)
    o = kraken.fetch_order(o["id"])
print("Quit")
sys.exit()

