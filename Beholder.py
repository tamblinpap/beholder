# This is the master beholder script
# Eventually this is the program you will run and all the features from other testing scripts will be implemented
#
# This bot and supplementary explanatory .py scripts where done by Tamblin Papendorp

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import math
from datetime import datetime
import datetime
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
userInput = ''
currentMode = ''


def SaveAsCSV(dataFrame):
    dataFrame.to_csv('Data/' + dataFrame + '.csv')


def ParseUserInput(inputStr):
    if inputStr == 'exit':
        return
    elif inputStr[0:2] == '-m':
        modeInput = inputStr[3:len(inputStr)]
        if modeInput == 'Test' or modeInput == 'test':
            ModeTest()
        elif modeInput == 'PaperTrade':
            ModePaperTrade()
        elif modeInput == 'ActualTrade':
            ModeActualTrade()
        else:
            print(modeInput + ' is not a valid mode, check the readme for help.')
    elif currentMode == 'test':
        if inputStr == 'menu':
            return
        elif inputStr[0:2] == '-g':
            GetData(inputStr[3:len(inputStr)])
        elif inputStr[0:3] == '-ls':
            print('\nPrice data available:')
            for file in os.listdir('Data'):
                if file[len(file)-4:len(file)] == '.csv':
                    print(file)
            print('\n')
        elif inputStr[0:2] == '-t':
            AlgoTester(inputStr[3:len(inputStr)])
        else:
            print('Not a valid command. Refer to readme on how to use test mode. type return to go back to menu')
    else:
        print('Not a valid command.')


def GetData(tickerCode):
    print('Attempting to get historical data for ' + tickerCode + '...')
    stock = yf.download(tickers=tickerCode, period='MAX')
    if len(stock) > 0:
        print('Found stock data for ' + tickerCode)
        stock.to_csv('Data/' + tickerCode + '_' + str(datetime.date.today()) + '_stats.csv')
    else:
        print('No stock data found for ' + tickerCode + '.  Trying crypto...')
    stock = yf.download(tickers=tickerCode + "-USD", period='MAX')
    if len(stock) > 0:
        print('Found crypto data for ' + tickerCode + '-USD')
        stock.to_csv('Data/' + tickerCode + '-USD_' + str(datetime.date.today()) + '_stats.csv')
    else:
        print('No crypto data was found for ' + tickerCode + '-USD.')


def AlgoTester(stockCSV):
    print('Preparing to test algorithms on ' + stockCSV[0:len(stockCSV) - 10] + '...')
    try:
        dataParsed = pd.read_csv('Data/' + stockCSV, index_col='Date')
    except:
        print('File name ' + stockCSV + ' does not exist in the Data folder, make sure you included .csv at the end.')
        return
    print('File ' + stockCSV + ' found and read.')
    # this statement makes sure data sheet rows are in the right order
    if pd.to_datetime(dataParsed.index[0]) > pd.to_datetime(dataParsed.index[len(dataParsed) - 1]):
        newTemp = pd.DataFrame(dataParsed.iloc[::-1])
        dataParsed = newTemp

    try:
        closePrice = dataParsed['Adj Close']
    except:
        closePrice = dataParsed['close']

    # converts the date strings in the index into pandas datetime format
    closePrice.index = pd.to_datetime(closePrice.index)

    # Creating the SMA's, WMA, and EMA
    tempSmaNum1 = 10
    tempSmaNum2 = 25
    tempSmaNum3 = 100

    smaFirst = closePrice.rolling(window=tempSmaNum1).mean()
    smaSecond = closePrice.rolling(window=tempSmaNum2).mean()
    smaThird = closePrice.rolling(window=tempSmaNum3).mean()
    weights = np.arange(1, tempSmaNum1 + 1)
    wma = closePrice.rolling(tempSmaNum1).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
    modPrice = closePrice.copy()
    modPrice.iloc[0:tempSmaNum1] = smaFirst[0:10]
    ema = modPrice.ewm(span=tempSmaNum1, adjust=False).mean()

    # Graphing the stats
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(12, 6))
    plt.plot(closePrice, label='Adj Close Price', linewidth=2)
    plt.plot(smaFirst, label=str(tempSmaNum1) + ' day rolling SMA', linewidth=1)
    plt.plot(smaSecond, label=str(tempSmaNum2) + ' day rolling SMA', linewidth=2)
    plt.plot(smaThird, label=str(tempSmaNum3) + ' day rolling SMA', linewidth=3)
    plt.plot(wma, label=str(tempSmaNum1) + ' day WMA', linewidth=2)
    plt.plot(ema, label=str(tempSmaNum1) + ' day EMA', linewidth=1)
    plt.xlabel('Date')
    plt.ylabel('Adjusted closing price ($USD)')
    plt.title(stockCSV[0:len(stockCSV) - 10] + ' Price with Moving Averages')
    plt.legend()

    MAPrice_df = pd.DataFrame({
        'Adj Close': closePrice,
        'SMA ' + str(tempSmaNum1): smaFirst,
        'SMA ' + str(tempSmaNum2): smaSecond,
        'SMA ' + str(tempSmaNum3): smaThird,
        'WMA10': np.round(wma, decimals=3),
        'EMA10': np.round(ema, decimals=3)
    })
    MACSVName = stockCSV[0:len(stockCSV) - 4] + '_MA.csv'
    MAPrice_df.to_csv('Data/MovingAvg/' + MACSVName)

    # Time to run tests
    dataParsed = pd.read_csv('Data/MovingAvg/' + MACSVName, index_col='Date')
    lastPrice = 0.0
    originalPrice = dataParsed.loc[dataParsed.index[0], dataParsed.columns[0]]
    dayNum = 1
    holdingsTemp = [['SMA', 100.0, 0.0], ['WMA', 100.0, 0.0], ['EMA', 100.0, 0.0]]
    holdings = pd.DataFrame(holdingsTemp, columns=['Type', 'USD', 'Shares'])

    print('\n\nStarting simulation of bot from ' + dataParsed.index[0] + ' to ' + dataParsed.index[len(dataParsed) - 1])
    for day in dataParsed.index:
        print('\nDay: ' + str(dayNum) + ' (' + day + ')')
        SMA1 = dataParsed.loc[day, dataParsed.columns[1]]
        SMA2 = dataParsed.loc[day, dataParsed.columns[2]]
        SMA3 = dataParsed.loc[day, dataParsed.columns[3]]
        WMA1 = dataParsed.loc[day, dataParsed.columns[4]]
        EMA1 = dataParsed.loc[day, dataParsed.columns[5]]

        differentAls = [SMA1, WMA1, EMA1]
        indexNum = 0

        lastPrice = dataParsed.loc[day, dataParsed.columns[0]]
        for Als in differentAls:
            if Als == SMA1:
                indexNum = 0
            elif Als == WMA1:
                indexNum = 1
            elif Als == EMA1:
                indexNum = 2
            if math.isnan(Als) or math.isnan(SMA2) or math.isnan(SMA3):
                print('Not enough data to trade with.')
            else:
                if Als > SMA2 and Als > SMA3 and holdings.loc[indexNum, 'USD'] > 0.0:
                    print('Buying Crypto/Stock at price of: $' + str(dataParsed.loc[day, dataParsed.columns[0]]))
                    holdings.loc[indexNum, 'Shares'] = holdings.loc[indexNum, 'USD'] / lastPrice
                    holdings.loc[indexNum, 'USD'] = 0.0
                    # tradeDates.append(day)
                elif Als < SMA2 or SMA1 < SMA3:
                    if holdings.loc[indexNum, 'Shares'] > 0.0:
                        print('Selling Crypto/Stock at price of: $' + str(dataParsed.loc[day, dataParsed.columns[0]]))
                        holdings.loc[indexNum, 'USD'] = lastPrice * holdings.loc[indexNum, 'Shares']
                        holdings.loc[indexNum, 'Shares'] = 0.0
                        # tradeDates.append(day)
                    else:
                        print('Holdings optimal, no buying or selling.')
                else:
                    print('Holdings optimal, no buying or selling.')

            print('Price: $' + str(lastPrice))
            print('USD holdings: ' + str(holdings.loc[indexNum, 'USD']))
            print('Crypto/Stock holdings: ' + str(holdings.loc[indexNum, 'Shares']) + '\n')
        dayNum = dayNum + 1

    print('\nDone!')
    # print('Bot placed trades on these days:')
    # print(tradeDates)
    for holdingsIndex in holdings.index:
        print('\nFor alg of ' + holdings.loc[holdingsIndex, 'Type'])
        if holdings.loc[holdingsIndex, 'USD'] > 0.0:
            print('Final value of portfolio ' + str(round(holdings.loc[holdingsIndex, 'USD'])) + '% of original with ' +
                  holdings.loc[holdingsIndex, 'Type'] + ' algo')
        else:
            print('Final value of portfolio ' + str(
                round(holdings.loc[holdingsIndex, 'Shares'] * lastPrice)) + '% of original with algo')
    print('\nIf no algo was implemented portfolio would be ' + str(
        round((lastPrice / originalPrice) * 100)) + '% of original\n')
    plt.show()


def ModeTest():
    global currentMode
    global userInput
    if currentMode != 'test':
        print('Launching in test mode...\n')
        print('Test mode is used mainly for testing the effectiveness of Beholder and its eyes on past data.')
        print('Test mode will run a simulation on all historical data available of a certain stock or crypto.')
        print('Enter ticker info for holding you would like to get historical info with -g.')
        print('Use -ls to list the imported stocks/crypto.\n')
        print('Test algos on data with -t "Datafile.csv"')
    currentMode = 'test'
    while userInput != 'return' and userInput != 'exit':
        print('BeholderCMD/Test: ', end='')
        userInput = input()
        ParseUserInput(userInput)
    print('Exiting test mode...')
    currentMode = 'main'


def ModePaperTrade():
    print('Launching in paper trade mode...')


def ModeActualTrade():
    print('Launching in actual trade mode...')


# Starting user interaction
if currentMode == '':
    beholderText = open('Info/Beholder.txt')
    for element in beholderText:
        print(element)
    print('Welcome to the "Beholder" bot!\n')
    print('Please refer to the README.md file for operation instructions')
    print(
        '\nThe creator of this bot is not liable for any losses or data theft that may happen as a result of this bot')
    print('The creator of this bot is not a financial advisor.  Use at your own risk')
    print('Beholder Bot was created by Tamblin Papendorp')
    print('\nWhat mode to you want to launch Beholder in?')

currentMode = 'menu'

while userInput != 'exit':
    print('BeholderCMD: ', end='')
    userInput = input()
    ParseUserInput(userInput)

print('\nGoodbye!')
sys.exit()
