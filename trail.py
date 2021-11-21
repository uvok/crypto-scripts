import sys
import time

import ccxt
from ccxt.base import errors as err

import config
import load
from custom_input import *

kraken = load.get_exchange()

oid = input("Order ID? ")
o = kraken.fetch_order(oid)
FACTOR = 0.99

while o["status"] == "open":
    print("Iterate")
    ob = kraken.fetch_order_book(o["symbol"], 1)
    sp = ob['bids'][0][0] * FACTOR

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

