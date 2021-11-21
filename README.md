# Quick and dirty crypto scripts

## Warning

**Obligatory Warning**: Software is provided as-is, might contain errors.
This might cause you to lose all your money. Proceed with caution.

## What is it?

Quick and dirty scripts I needed to deal with Kraken (easier).
Might be adjustable to other exchanges.

- cancel.py:
  Track margin orders, i.e. opposed take-profit and stop-loss orders.
  Kraken unfortunately doesn't provide OCO orders, so I had to script it myself.
  
  In order tp prevent closing a position and opening a new one some time later.
  
  This is not relevant to regular orders, since Kraken and Bitpanda immediately
  lock assets in one order. So you can't have both regular stop-loss and take-profit
  orders.
  
  Personally, I workaround this by running freqtrade with forcebuy.
- setlimit.py:
  script for buying a coin and immediately placing limit orders
  of a quarter amount each at 1-2-3-4 % price gains. No idea if that
  makes sense IRL. I want to take "as much profit as possible", by also
  using early chances.
  
  Again, freqtrade might be a better option.
- trail.py:
  Manual trailing stop loss *for margin*.
  Places 'leverage' argument (probably only for Kraken?)

## Requirements

- Python 3, tested with 3.7
- some current version of ccxt

