import sys
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

oid = input("Order ID?")

while o["status"] == "open":
    o = kraken.fetch_order(oid)
    oid = o["id"]
    ob = kraken.fetch_order_book(o["symbol"], 1)
    sp = ob['bids'][0][0] * 0.995

    if o["price"] < sp:
        print(f"Update order to new sell price {sp} in 3 seconds")
        time.sleep(3)
        kraken.cancel_order(o["id"])
        o = kraken.create_order(o["symbol"], "stop-loss", "sell", o["amount"], sp, { "leverage":"5" } )
    time.sleep(30)
sys.exit()

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
    
try:
    import questionaryx
    vprompt=1
except ImportError:
    vprompt=0
import config

kraken = ccxt.kraken({
#        "apiKey": config.APIKEY,
#        "secret": config.SECRET,
#        "enableRateLimit": True,
})

#kraken.checkRequiredCredentials()

def my_input(query):
    if vprompt:
        return questionary.text(query).ask()
    else:
        return input(query+" ")

def my_select(query, options):
    if vprompt:
        return questionary.select(
            query,
            choices=options
        ).ask()
    else:
        txt = f"{query} ({', '.join(options)}) "
        return input(txt)

def my_confirm(query):
    if vprompt:
        return questionary.confirm(query, default=False, auto_enter=False).ask()
    else:
        reply = my_input(query)
        reply = reply.lower()[0]
        return reply[0] == "y"


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

