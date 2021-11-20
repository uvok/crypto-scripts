import sys
from pprint import pprint as pp
import time
import ccxt
from ccxt.base import errors as err
import config

kraken = ccxt.kraken({
        "apiKey": config.APIKEY,
        "secret": config.SECRET,
        "enableRateLimit": True,
})

kraken.checkRequiredCredentials()

pair = input("Enter currency pair: ")

def get_market_price(exchange, pair):
    # limit to 1
    orderbook = exchange.fetch_order_book(pair, 1)
    bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
    ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
    spread = (ask - bid) if (bid and ask) else None
    return [bid, ask, spread]

print("Current market: ")
prices = get_market_price(kraken, pair)
print(prices)

curr = ""
while not curr in ["C","F"]:
    curr = input("Currency, *F*iat or *C*rypto?")

amout = input("Amount to buy? ")
amout = float(amout)

buyprice = prices[1]
if curr == "C":
    # nothing to do
    pass
elif curr == "F":
    amout = amout / buyprice
    amout = round(amout, 6)

reply = input(f"Buying {amout} from {pair}, okay? ")

if reply != "y":
    sys.exit()

result = kraken.createMarketBuyOrder(pair, amout)
print(result)

reply = input("Create 1-2-3-4 % limit sell orders? ")

if reply != "y":
    sys.exit()

for incr in range(1,5):
    sellp = buyprice * (1 + incr / 100)
    print(f"Creating {incr} % sell order @ {sellp}")
    res = kraken.createLimitSellOrder(pair, amout / 4, sellp)
    print(res)

