import sys
import time

import ccxt
from ccxt.base import errors as err

import config
import load
from custom_input import *

kraken = load.get_exchange()

def get_market_price(exchange, pair):
    # limit to 1
    orderbook = exchange.fetch_order_book(pair, 1)
    bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
    spread = (ask - bid) if (bid and ask) else None
    return [bid, ask, spread]


valid_sym=False
while not valid_sym:
    try:
        pair = my_input("Enter currency pair:")
        print("Current market: ")
        prices = get_market_price(kraken, pair)
        print(prices)
        valid_sym = True
    except err.BadSymbol:
        print("Invalid pair")

curr = ""
while not curr in ["C","F"]:
    a = my_select("Unit for specifying buy?", ["Fiat", "Crypto"])
    curr = a[0]

amout = my_input("Amount to buy?")
amout = float(amout)

buyprice = prices[1]
if curr == "C":
    # nothing to do
    pass
elif curr == "F":
    amout = amout / buyprice
    amout = round(amout, 6)

reply = my_confirm(f"Buying {amout} from {pair}, okay?")

if not reply:
    print("Aborting")
    sys.exit()

result = kraken.createMarketBuyOrder(pair, amout)
print(result)

reply = my_confirm("Create 1-2-3-4 % limit sell orders?")
if not reply:
    print("Aborting")
    sys.exit()

for incr in range(1,5):
    sellp = buyprice * (1 + incr / 100)
    print(f"Creating {incr} % sell order @ {sellp}")
    res = kraken.createLimitSellOrder(pair, amout / 4, sellp)
    print(res)

