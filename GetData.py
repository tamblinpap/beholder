import yfinance as yf
import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime

cg = CoinGeckoAPI()
print('Type Stock/BTC symbol for information: ', end='')
tickerCode = input()

stock = yf.download(tickers=tickerCode, period='MAX')
if len(stock) > 0:
    print('Import Successful')
else:
    print("\nNot a stock, trying crypto...")
    stock = yf.download(tickers=tickerCode + "-USD", period='MAX')
    print('Import Successful')

stock.to_csv('Data/' + tickerCode + '_stats.csv')