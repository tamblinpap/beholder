import numpy as np #The Numpy numerical computing library
from datetime import datetime
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for
import math #The Python math module
from pycoingecko import CoinGeckoAPI #grabs live crypto prices

cg = CoinGeckoAPI()
BTCPrice = cg.get_price(ids='bitcoin', vs_currencies='usd', include_last_updated_at='true')
lastPrice = None
currentTime = datetime.now()
lastMin = currentTime.minute

num = 1
print('\n\n\n')
print(cg.ping())
print('This script calls a get price request from the CoinGeckoAPI every 5 minutes')

#this runs every tick until stoped and to check the price
while num == 1:
    currentTime = datetime.now()
    if abs(currentTime.minute-lastMin) > 4:
        lastMin = currentTime.minute
        print('Tried to get price at: ', end='')
        print(currentTime)
        BTCPrice = cg.get_price(ids='bitcoin', vs_currencies='usd', include_last_updated_at='true')
    if BTCPrice["bitcoin"]['last_updated_at'] != lastPrice:
        lastPrice = BTCPrice['bitcoin']['last_updated_at']
        print('Bitcoin Price: ', end='')
        print(BTCPrice['bitcoin']['usd'])
        timeVar = datetime.now()
        print('Current Time/Date: ', timeVar, '\n')