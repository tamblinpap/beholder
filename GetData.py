import yfinance as yf
import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime

cg = CoinGeckoAPI()
print('Type Stock/BTC symbol for information: ', end='')
tickerCode = input()
ticker = yf.Ticker(tickerCode)
print(ticker.recommendations)
print(len(ticker.recommendations))

stock = yf.download(tickers=tickerCode, period='MAX')
if len(stock) > 0:
    print('Found stock data for ' + tickerCode)
    stock.to_csv('Data/' + tickerCode + '_stats.csv')
else:
    print('No stock data found for ' + tickerCode + '.  Trying crypto...')
stock = yf.download(tickers=tickerCode + "-USD", period='MAX')
if len(stock) > 0:
    print('Found crypto data for ' + tickerCode + '-USD')
    stock.to_csv('Data/' + tickerCode + '-USD_stats.csv')
else:
    print('No crypto data was found for ' + tickerCode + '-USD.')

