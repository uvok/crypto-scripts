from pprint import pprint as pp
import time
import ccxt
from ccxt.base import errors as err
import config
import sys

pair = None
if len(sys.argv) == 2:
    pair = sys.argv[1]


kraken = ccxt.kraken({
        "apiKey": config.APIKEY,
        "secret": config.SECRET,
        "enableRateLimit": True,
})

kraken.checkRequiredCredentials()

orders = kraken.fetchOpenOrders(pair)

for o in orders:
    print(f"{o['datetime']} {o['side']:<6} {o['type']:<12} {o['id']} {o['symbol']:<10} {o['amount']} @  {o['price']}")

oids = [o['id'] for o in orders]
track_pairs = []
track_all = []
curr_pairs = []
print("Enter orders to track. Empty to finish. n for next pair.")

while True:
    inp = input("> ")
    if inp == "n" or inp == "":
        if curr_pairs:
            track_pairs.append(curr_pairs)
        curr_pairs = []
    elif inp in track_all:
        print("Already present")
        continue
    elif inp in oids:
        track_all.append(inp)
        curr_pairs.append(inp)
    else:
        print("Invalid input")

    if inp == "":
        break

print(f"Tracking {track_pairs}")

while True:
    try:
        print("----")
        oo = kraken.fetch_open_orders()
        co = kraken.fetch_closed_orders()
        remove_candidates = []

        if not track_pairs:
            break

        for pairs in track_pairs:
            print(f"Checking {pairs}")
            orders = [o for o in (oo + co) if o["id"] in pairs]
            if len(orders) != len(pairs):
                print(f"Error: Different lengths for order candiates ( {len(pairs)} ) and found orders ( {len(orders)} ).")
                # skip pair to avoid doing bad operations
                continue

            closed = [o for o in orders if o["status"] != "open"]
            opened = [o for o in orders if o["status"] == "open"]
            print(f"{len(closed)} non-open and {len(opened)} open orders")
            if len(closed) > 0:
                print("Non-open:")
                for c in closed:
                    print(c["id"])

                print("Non-Open order(s) found, closing remaining opens in 10s...")
                time.sleep(10)

                print("Open:")
                for o in opened:
                    print(f"Cancel {o["id"]}")
                    kraken.cancel_order(o["id"])
                remove_candidates.append(pairs)
        ## for pair in track_pairs
        for rc in remove_candidates:
            print(f"Finished with {rc}, removing")
            try:
                track_pairs.remove(rc)
            except ValueError:
                print(f"Error: Removing pair {rc} not possible")
    except err.NetworkError:
        print("Network error!")
    time.sleep(60)
