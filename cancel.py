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

orders = kraken.fetchOpenOrders()

for o in orders:
    print(f"{o['datetime']} {o['side']:<6} {o['type']:<12} {o['id']} {o['symbol']:<10} {o['amount']} @  {o['price']}")

oids = [o['id'] for o in orders]
track = []
print("Enter orders to track. Empty to finish.")

while True:
    inp = input("> ")
    if inp == "":
        break
    elif inp in track:
        print("Already present")
        continue
    elif inp in oids:
        track.append(inp)
    else:
        print("Invalid input")

print(f"Tracking {track}")

while True:
    try:
        print("----")
        curr = []
        for o in track:
            order = kraken.fetch_order(o)
            print(f"{order['id']}: {order['status']}")
            curr.append(order)
        closed = [o for o in curr if o["status"] != "open"]
        opened = [o for o in curr if o["status"] == "open"]
        print(f"{len(closed)} non-open and {len(opened)} open orders")
        if len(closed) > 0:
            print("Non-Open order found, closing remaining opens in 10s...")
            time.sleep(10)
            print("Non-open:")
            for c in closed:
                print(c["id"])
            print("Open:")
            for o in opened:
                print(o["id"])
                kraken.cancel_order(o["id"])
            break
    except err.NetworkError:
        print("Network error!")
    time.sleep(60)
