# This is the master beholder script
# Eventually this is the program you will run and all the features from other testing scripts will be implemented
#
# This bot and supplementary explanatory .py scripts where done by Tamblin Papendorp
# This line is testing my github

# lib imports
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import math
import datetime
from pycoingecko import CoinGeckoAPI
from webull import webull
from webull import paper_webull

cg = CoinGeckoAPI()
pwb = paper_webull()
wb = webull()
userInput = ''
currentMode = ''
availableMoney = 0.0
lastLook = datetime.date.min

# Saves as CSV
def SaveAsCSV(dataFrame):
    dataFrame.to_csv('Data/' + dataFrame + '.csv')


# This method parses and organizes webull acount information in a readable way
def PrintAccountInfo(accountInfo):
    # This function prints the data from a webull account in readable way and saves the tickers for the account
    tickerList = [] * 0
    print('\n\nACCOUNT INFO')
    try:
        print('Account type: ' + accountInfo['accounts'][0]['paperName'])
        isPaper = True
    except:
        print('Account type: Real ' + accountInfo['currency'])
        isPaper = False
    print('Total Account Value: ' + accountInfo['netLiquidation'])
    print('-(' + str(
        round(float(accountInfo['accountMembers'][1]['value']) / float(accountInfo['netLiquidation']) * 100,
              1)) + '%) Money in cash: ' + accountInfo['accountMembers'][1]['value'])
    print('-(' + str(
        round(float(accountInfo['accountMembers'][0]['value']) / float(accountInfo['netLiquidation']) * 100,
              1)) + '%) Money in holdings: ' + accountInfo['accountMembers'][0]['value'])
    if isPaper:
        for i in accountInfo['positions']:
            tickerList.append(i['ticker']['symbol'])
            print('   >(' + str(
                round((float(i['marketValue']) / float(accountInfo['accountMembers'][0]['value'])) * 100,
                      1)) + '%) ' + str(i['position']) + ' share(s) of ' + i['ticker']['symbol'] + ' at $' + i[
                      'lastPrice'] + ' each')
    else:
        for i in accountInfo['positions']:
            tickerList.append(i['ticker']['symbol'])
            if i['assetType'] == 'stock':
                print('   >(' + str(
                    round((float(i['marketValue']) / float(accountInfo['accountMembers'][0]['value'])) * 100,
                          1)) + '%) ' + str(i['position']) + ' share(s) of ' + i['ticker']['symbol'] + ' at $' + i[
                          'lastPrice'] + ' each')
            elif i['assetType'] == 'crypto':
                print('   >(' + str(
                    round((float(i['marketValue']) / float(accountInfo['accountMembers'][0]['value'])) * 100,
                          1)) + '%) ' + str(i['position']) + ' ' + i['ticker']['symbol'] + ' at $' + i['marketValue'])
    if accountInfo['openOrderSize'] > 0:
        print('Open Orders: ')
        for i in accountInfo['openOrders']:
            try:
                print('   >' + i['action'] + 'ING ' + str(
                    round(float(i['totalQuantity']) - float(i['filledQuantity']))) + ' of ' + i[
                          'totalQuantity'] + ' of ' + i['ticker']['tinyName'] + '(' + i['ticker'][
                          'symbol'] + ') for $' + i['lmtPrice'] + ' a share.')
            except:
                print('   >' + i['action'] + 'ING ' + str(
                    round(float(i['totalQuantity']) - float(i['filledQuantity']))) + ' of ' + i[
                          'totalQuantity'] + ' of ' + i['ticker']['tinyName'] + '(' + i['ticker'][
                          'symbol'] + ') for market price')
    else:
        print('No Open Orders.')
    print('\n')
    if isPaper:
        with open("Info/Paper/Tickers.txt", "w") as output:
            for ticker in tickerList:
                output.write(ticker + '\n')
    else:
        with open("Info/Normal/Tickers.txt", "w") as output:
            for ticker in tickerList:
                output.write(ticker + '\n')


# This method prints instructions to the user
def Help():
    print('\n\nBEHOLDER HELP\n')
    print('MODE MAIN:')
    print('="exit" closes the program')
    print('="-m" is the pointer to enter a mode. Modes available are test, paper, and normal. Ex."-m test" ')
    print('="menu" or "return" will return to main menu from any other mode')
    print('MODE TEST:')
    print('="-g" is the pointer to get ticker data. It is called with a ticker id after the pointer. Ex."-g MSFT"')
    print('="-ls" lists all of the ticker data files available.')
    print('="-t" is the pointer to test historical data with the Beholder algorithm. It is called with ticker id or .csv path. Ex."-t MSFT" or "-t MSFT_2021-02-23_stats.csv"')
    print('MODE PAPER:')
    print('This mode uses webull paper trading to simulate trading. The differences between paper and normal mode is in paper mode, crypto trading is not supported and money is simulated.')
    print('="-ls" will reprint account info and holdings')
    print('="-t" will run the Beholder algorithm on all account holdings')
    print('MODE NORMAL:')
    print('This mode connects to your webull account and uses real money and holdings.  No trades will be made without you allowing Beholder to do so.')
    print('="-ls" will reprint account info and holdings')
    print('="-t" will run the Beholder algorithm on all account holdings')


# This method handles the commands for all modes
def ParseUserInput(inputStr):
    if inputStr == 'exit':
        return
    elif inputStr == '-help' or inputStr == '-h' or inputStr == 'help':
        Help()
    elif inputStr[0:2] == '-m' and currentMode == 'menu':
        modeInput = inputStr[3:len(inputStr)]
        if modeInput == 'Test' or modeInput == 'test':
            ModeTest()
        elif modeInput == 'Paper' or modeInput == 'paper':
            ModePaperTrade()
        elif modeInput == 'Normal' or modeInput == 'normal':
            ModeActualTrade()
        else:
            print(modeInput + ' is not a valid mode, check the readme or use "-help" for help.')
    elif currentMode == 'test':
        if inputStr == 'menu' or inputStr == 'return':
            return
        elif inputStr[0:2] == '-g':
            GetData(inputStr[3:len(inputStr)], False)
        elif inputStr[0:3] == '-ls':
            print('\nPrice data available:')
            for file in os.listdir('Data'):
                if file[len(file) - 4:len(file)] == '.csv':
                    print(file)
            print('\n')
        elif inputStr[0:2] == '-t':
            AlgoTester(inputStr[3:len(inputStr)], False)
        else:
            print('Not a valid command. Refer to readme on how to use test mode. type return to go back to menu')
    elif currentMode == 'paper':
        if inputStr == 'watch':
            return
        elif inputStr == 'return' or inputStr == 'menu':
            return
        elif inputStr[0:3] == '-ls':
            PrintAccountInfo(pwb.get_account())
        elif inputStr[0:2] == '-t':
            AlgoTester(GetDataList('paper'), True)
        elif inputStr[0:4] == '-add':
            WatchedTickerList(inputStr[1:4], inputStr[5:len(inputStr)])
        elif inputStr[0:3] == '-rm':
            WatchedTickerList(inputStr[1:3], inputStr[4:len(inputStr)])
    elif currentMode == 'normal':
        if inputStr == 'watch':
            return
        elif inputStr == 'return' or inputStr == 'menu':
            return
        elif inputStr[0:3] == '-ls':
            PrintAccountInfo(wb.get_account())
        elif inputStr[0:2] == '-t':
            AlgoTester(GetDataList('normal'), True)
        elif inputStr[0:4] == '-add':
            WatchedTickerList(inputStr[1:4], inputStr[5:len(inputStr)])
        elif inputStr[0:3] == '-rm':
            WatchedTickerList(inputStr[1:3], inputStr[4:len(inputStr)])
    else:
        print('Not a valid command.')


# This method reads in a list of data, formats it, and then sends it through GetData()
def GetDataList(accountType):
    # gets ticker csv files for a webull portfolio (either normal or paper)
    if accountType == 'paper':
        tickerText = open('Info/Paper/Tickers.txt')
    elif accountType == 'normal':
        tickerText = open('Info/Normal/Tickers.txt')
    else:
        print('Error not in paper of normal trading mode')
        return
    with tickerText as f:
        tickerList = f.readlines()
    for tickerCode in tickerList:
        GetData(tickerCode, False)
    # returns list of tickers
    return tickerList


# This method pulls csv files from the yahoo finance API and saves them as csv files
def GetData(tickerC, isQuiet):
    # gets ticker csv files and deletes old ones
    if type(tickerC) == type('string'):
        tickerCode = tickerC
        if tickerCode == '' or tickerCode == '\n' or tickerCode == ' ':
            return
        if tickerCode[len(tickerCode) - 1:len(tickerCode)] == '\n':
            tickerCode = tickerCode[0:len(tickerCode) - 1]
        if tickerCode[len(tickerCode) - 3:len(tickerCode)] == 'USD' and tickerCode[
                                                                        len(tickerCode) - 4:len(tickerCode) - 3] != '-':
            tickerCode = tickerCode[0:len(tickerCode) - 3]
            print(tickerCode)
        if not isQuiet:
            print('Attempting to get historical data for ' + tickerCode + '...')
        stock = yf.download(tickers=tickerCode, period='MAX')
        if len(stock) > 0:
            if not isQuiet:
                print('Found stock data for ' + tickerCode)
            stockSaveName = 'Data/' + tickerCode + '_' + str(datetime.date.today()) + '_stats.csv'
            for file in os.listdir('Data'):
                if file[len(file) - 9:len(file)] == 'stats.csv':
                    if file[0:len(tickerCode)] == tickerCode and file[len(tickerCode):len(tickerCode) + 1] != '-':
                        os.remove('Data/' + file)
            stock.to_csv(stockSaveName)
        else:
            if not isQuiet:
                print('No stock data found for ' + tickerCode + '.  Trying crypto...')
        stock = yf.download(tickers=tickerCode + "-USD", period='MAX')
        if len(stock) > 0:
            if not isQuiet:
                print('Found crypto data for ' + tickerCode + '-USD')
            stockSaveName = 'Data/' + tickerCode + '-USD_' + str(datetime.date.today()) + '_stats.csv'
            for file in os.listdir('Data'):
                if file[len(file) - 9:len(file)] == 'stats.csv':
                    if file[0:len(tickerCode)] == tickerCode and file[len(tickerCode):len(tickerCode) + 1] == '-':
                        os.remove('Data/' + file)
            stock.to_csv(stockSaveName)
        else:
            if not isQuiet:
                print('No crypto data was found for ' + tickerCode + '-USD.')
    else:
        for x in tickerC:
            GetData(x, isQuiet)


# This method runs all the data analysis algorithms on a ticker or list of tickers
def AlgoTester(stockCSV, isQuiet):
    if type(stockCSV) == type('string'):
        if stockCSV[len(stockCSV) - 1:len(stockCSV)] == '\n':
            stockCSV = stockCSV[0:len(stockCSV) - 1]
        print('Preparing to test algorithms on ' + stockCSV + '...')
        try:
            dataParsed = pd.read_csv('Data/' + stockCSV, index_col='Date')
        except:
            try:
                print('Not a csv file, looking for files with similar ticker indicators...')
                if stockCSV[len(stockCSV) - 3:len(stockCSV)] == 'USD' and stockCSV[
                                                                          len(stockCSV) - 4:len(stockCSV) - 3] != '-':
                    stockCSV = stockCSV[0:len(stockCSV) - 3] + '-' + stockCSV[len(stockCSV) - 3:len(stockCSV)]
                for file in os.listdir('Data'):
                    if file[len(file) - 9:len(file)] == 'stats.csv':
                        if file[0:len(stockCSV)] == stockCSV:
                            print(file)
                            dataParsed = pd.read_csv('Data/' + file, index_col='Date')
            except:
                print('Data file for ' + stockCSV + ' does not exist in the Data folder.')
                return
        if not isQuiet:
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

        # Creating the RSI
        RSI_WINDOW = 14

        percentGains = []
        percentLosses = []
        lastPrice = 0.0
        for day in closePrice.index:
            currentPrice = closePrice[day]
            if lastPrice == 0.0:
                lastPrice = currentPrice
                percentGains.append(0.0)
                percentLosses.append(0.0)
                continue
            if currentPrice / lastPrice < 1.0:
                percentGains.append(0.0)
                percentLosses.append(round((1 - (currentPrice / lastPrice)) * 100, 2))
            elif currentPrice / lastPrice > 1.0:
                percentLosses.append(0.0)
                percentGains.append(round(((currentPrice / lastPrice) - 1) * 100, 2))
            else:
                percentGains.append(0.0)
                percentLosses.append(0.0)
            lastPrice = currentPrice
        RSIPrice_df = pd.DataFrame({
            'Price': closePrice,
            'Gains': percentGains,
            'Losses': percentLosses,
        })
        rolling_gain = RSIPrice_df['Gains'].rolling(RSI_WINDOW).mean()
        rolling_loss = RSIPrice_df['Losses'].rolling(RSI_WINDOW).mean()
        RSIPrice_df['RSI'] = 100 - (100 / ((rolling_gain / rolling_loss) + 1))

        # Creating the MACD and Signal Lines
        emaNum1 = 12
        emaNum2 = 26
        sigLineNum = 9

        exp1 = closePrice.ewm(span=emaNum1, adjust=False).mean()
        exp2 = closePrice.ewm(span=emaNum2, adjust=False).mean()
        macd = exp1-exp2
        sigLine = macd.ewm(span=sigLineNum, adjust=False).mean()

        # Creating the SMA, WMA, and EMA
        tempMANum1 = 10
        tempMANum2 = 20
        tempMANum3 = 100

        smaFirst = closePrice.rolling(window=tempMANum1).mean()
        smaSecond = closePrice.rolling(window=tempMANum2).mean()
        smaThird = closePrice.rolling(window=tempMANum3).mean()
        weights = np.arange(1, tempMANum1 + 1)
        wma = closePrice.rolling(tempMANum1).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)
        modPrice = closePrice.copy()
        modPrice.iloc[0:tempMANum1] = smaFirst[0:tempMANum1]
        ema = modPrice.ewm(span=tempMANum1, adjust=False).mean()

        # Graphing the stats
        if not isQuiet:
            plt.style.use('fivethirtyeight')
            plt.figure(figsize=(10, 5))
            plt.plot(closePrice, label='Adj Close Price', linewidth=2)

            # plt.plot(smaFirst, label=str(tempMANum1) + ' day SMA', linewidth=1)
            # plt.plot(smaSecond, label=str(tempMANum2) + ' day SMA', linewidth=2)
            # plt.plot(smaThird, label=str(tempMANum3) + ' day SMA', linewidth=3)
            # plt.plot(wma, label=str(tempMANum1) + ' day WMA', linewidth=2)
            # plt.plot(ema, label=str(tempMANum1) + ' day EMA', linewidth=1)
            plt.xlabel('Date')
            plt.ylabel('Adjusted closing price ($USD)')
            plt.title(stockCSV[0:4] + ' Analysis')
            plt.legend()
            plt.show()

            plt.style.use('fivethirtyeight')
            plt.figure(figsize=(10, 5))
            plt.plot(macd, label='MACD', linewidth=2)
            plt.plot(sigLine, label=str(sigLineNum) + ' day Signal Line', linewidth=2)
            plt.plot(RSIPrice_df['RSI'], label='RSI', linewidth=2)
            plt.title('RSI and MACD')
            plt.show()

        analyzedPrice_df = pd.DataFrame({
            'Adj Close': closePrice,
            'SMA ' + str(tempMANum1): smaFirst,
            'SMA ' + str(tempMANum2): smaSecond,
            'SMA ' + str(tempMANum3): smaThird,
            'WMA10': np.round(wma, decimals=3),
            'EMA10': np.round(ema, decimals=3),
            'RSI': RSIPrice_df['RSI'],
            'MACD': macd,
            str(sigLineNum) + ' DAY SIGNAL LINE': sigLine,
            'ALGO/VERDICT': None
        })
        AnalyzedCSVName = stockCSV[0:len(stockCSV)] + '_' + str(datetime.date.today()) + '_ANALYZED.csv'
        analyzedPrice_df.to_csv('Data/Analyzed/' + AnalyzedCSVName)

        # Time to run tests
        dataParsed = pd.read_csv('Data/Analyzed/' + AnalyzedCSVName, index_col='Date')
        lastPrice = 0.0
        originalPrice = dataParsed.loc[dataParsed.index[0], dataParsed.columns[0]]
        dayNum = 1
        holdingsTemp = [['RSI', 100.0, 0.0], ['MACD', 100.0, 0.0], ['WEIGHT', 100.0, 0.0]]
        holdings = pd.DataFrame(holdingsTemp, columns=['Type', 'USD', 'Shares'])
        tempData = [[0.0, 'N/A'], [0.0, 'N/A'], [0.0, 'N/A'], [0.0, 'N/A']]
        lastAlgoValues = pd.DataFrame(tempData, columns=['Value', 'Verdict'], index=['RSI', 'MACD', 'sigLine', 'WEIGHT'])

        seerersIndex = 0.0
        RSIWeight = 0.0
        MACDWeight = 0.0

        if not isQuiet:
            print('\n\nStarting simulation of bot from ' + dataParsed.index[0] + ' to ' + dataParsed.index[
                len(dataParsed) - 1])
        for day in dataParsed.index:
            if not isQuiet:
                print('\nDay: ' + str(dayNum) + ' (' + day + ')')
            SMA1 = dataParsed.loc[day, dataParsed.columns[1]]
            SMA2 = dataParsed.loc[day, dataParsed.columns[2]]
            SMA3 = dataParsed.loc[day, dataParsed.columns[3]]
            WMA1 = dataParsed.loc[day, dataParsed.columns[4]]
            EMA1 = dataParsed.loc[day, dataParsed.columns[5]]
            RSI = dataParsed.loc[day, dataParsed.columns[6]]
            MACD = dataParsed.loc[day, dataParsed.columns[7]]
            sigLine = dataParsed.loc[day, dataParsed.columns[8]]

            lastAlgoValues.loc['RSI', 'Value'] = RSI
            lastAlgoValues.loc['MACD', 'Value'] = MACD
            lastAlgoValues.loc['sigLine', 'Value'] = sigLine
            differentAls = [RSI, MACD, sigLine]
            indexNum = 0
            lastPrice = dataParsed.loc[day, dataParsed.columns[0]]

            if math.isnan(RSI) or math.isnan(MACD) or math.isnan(sigLine):
                if not isQuiet:
                    print('Not enough data to trade with.')
            else:
                if MACD > sigLine:
                    lastAlgoValues.loc['MACD', 'Verdict'] = 'BUY'
                    MACDWeight = 10
                    if holdings.loc[1, 'USD'] > 0.0:
                        if not isQuiet:
                            print(
                                'Buying Crypto/Stock at price of: $' + str(dataParsed.loc[day, dataParsed.columns[0]]))
                        holdings.loc[1, 'Shares'] = holdings.loc[1, 'USD'] / lastPrice
                        holdings.loc[1, 'USD'] = 0.0
                    else:
                        if not isQuiet:
                            print('Holdings optimal, no buying or selling.')
                elif MACD < sigLine:
                    lastAlgoValues.loc['MACD', 'Verdict'] = 'SELL'
                    MACDWeight = -10
                    if holdings.loc[1, 'Shares'] > 0.0:
                        if not isQuiet:
                            print('Selling Crypto/Stock at price of: $' + str(
                                dataParsed.loc[day, dataParsed.columns[0]]))
                        holdings.loc[1, 'USD'] = lastPrice * holdings.loc[1, 'Shares']
                        holdings.loc[1, 'Shares'] = 0.0
                    else:
                        if not isQuiet:
                            print('Holdings optimal, no buying or selling.')
                if RSI < 20:
                    lastAlgoValues.loc['RSI', 'Verdict'] = 'BUY'
                    RSIWeight = 1
                    if holdings.loc[indexNum, 'USD'] > 0.0:
                        if not isQuiet:
                            print(
                                'Buying Crypto/Stock at price of: $' + str(dataParsed.loc[day, dataParsed.columns[0]]))
                        holdings.loc[indexNum, 'Shares'] = holdings.loc[indexNum, 'USD'] / lastPrice
                        holdings.loc[indexNum, 'USD'] = 0.0
                    else:
                        if not isQuiet:
                            print('Holdings optimal, no buying or selling.')
                elif 50 > RSI > 20:
                    lastAlgoValues.loc['RSI', 'Verdict'] = 'BUY'
                    RSIWeight = 0
                    if holdings.loc[indexNum, 'USD'] > 0.0:
                        if not isQuiet:
                            print(
                                'Buying Crypto/Stock at price of: $' + str(dataParsed.loc[day, dataParsed.columns[0]]))
                        holdings.loc[indexNum, 'Shares'] = holdings.loc[indexNum, 'USD'] / lastPrice
                        holdings.loc[indexNum, 'USD'] = 0.0
                    else:
                        if not isQuiet:
                            print('Holdings optimal, no buying or selling.')
                elif RSI > 90:
                    lastAlgoValues.loc['RSI', 'Verdict'] = 'SELL'
                    RSIWeight = -1
                    if holdings.loc[indexNum, 'Shares'] > 0.0:
                        if not isQuiet:
                            print('Selling Crypto/Stock at price of: $' + str(
                                dataParsed.loc[day, dataParsed.columns[0]]))
                        holdings.loc[indexNum, 'USD'] = lastPrice * holdings.loc[indexNum, 'Shares']
                        holdings.loc[indexNum, 'Shares'] = 0.0
                    else:
                        if not isQuiet:
                            print('Holdings optimal, no buying or selling.')
                # Start Weighting
                seerersIndex = RSIWeight + MACDWeight
                lastAlgoValues.loc['WEIGHT', 'Value'] = seerersIndex
                if seerersIndex >= 10:
                    lastAlgoValues.loc['WEIGHT', 'Verdict'] = 'BUY'
                    if holdings.loc[2, 'USD'] > 0.0:
                        if not isQuiet:
                            print(
                                'Buying Crypto/Stock at price of: $' + str(dataParsed.loc[day, dataParsed.columns[0]]))
                        holdings.loc[2, 'Shares'] = holdings.loc[2, 'USD'] / lastPrice
                        holdings.loc[2, 'USD'] = 0.0
                elif seerersIndex <= -10:
                    lastAlgoValues.loc['WEIGHT', 'Verdict'] = 'SELL'
                    if holdings.loc[2, 'Shares'] > 0.0:
                        if not isQuiet:
                            print('Selling Crypto/Stock at price of: $' + str(
                                dataParsed.loc[day, dataParsed.columns[0]]))
                        holdings.loc[2, 'USD'] = lastPrice * holdings.loc[2, 'Shares']
                        holdings.loc[2, 'Shares'] = 0.0
            if not isQuiet:
                print('Price: $' + str(lastPrice))
                print('USD holdings for RSI: ' + str(holdings.loc[indexNum, 'USD']))
                print('Crypto/Stock holdings for RSI: ' + str(holdings.loc[indexNum, 'Shares']) + '\n')
                print('USD holdings for MACD: ' + str(holdings.loc[1, 'USD']))
                print('Crypto/Stock holdings for MACD: ' + str(holdings.loc[1, 'Shares']) + '\n')
            dayNum = dayNum + 1

        print('\nDone!')
        # print('Bot placed trades on these days:')
        # print(tradeDates)
        verdict = ''
        bestAlgo = ''
        bestAlgoNum = 0.0
        for holdingsIndex in holdings.index:
            print('For alg of ' + holdings.loc[holdingsIndex, 'Type'])
            tempAlgo = holdings.loc[holdingsIndex, 'Type']
            if holdings.loc[holdingsIndex, 'USD'] > 0.0:
                tempAlgoNum = round(holdings.loc[holdingsIndex, 'USD'])
                print('Final value of portfolio ' + str(tempAlgoNum) + '% of original with ' + tempAlgo + ' algo')
            else:
                tempAlgoNum = round(holdings.loc[holdingsIndex, 'Shares'] * lastPrice)
                print('Final value of portfolio ' + str(tempAlgoNum) + '% of original with' + tempAlgo + 'algo')
            if tempAlgoNum > bestAlgoNum:
                bestAlgoNum = tempAlgoNum
                bestAlgo = tempAlgo
        print('\nIf no algo was implemented portfolio would be ' + str(
            round((lastPrice / originalPrice) * 100)) + '% of original\n')
        verdict = lastAlgoValues.loc[bestAlgo, 'Verdict']
        print('Verdict today with ' + bestAlgo + ' algo: ' + verdict + '\n')
        analyzedPrice_df = pd.DataFrame({
            'Adj Close': closePrice,
            'SMA ' + str(tempMANum1): smaFirst,
            'SMA ' + str(tempMANum2): smaSecond,
            'SMA ' + str(tempMANum3): smaThird,
            'WMA10': np.round(wma, decimals=3),
            'EMA10': np.round(ema, decimals=3),
            'RSI': RSIPrice_df['RSI'],
            'MACD': macd,
            str(sigLineNum) + ' DAY SIGNAL LINE': sigLine,
            'ALGO/VERDICT': bestAlgo + ':' + verdict
        })
        analyzedPrice_df.to_csv('Data/Analyzed/' + AnalyzedCSVName)
    elif type(stockCSV) == list:
        print('Preparing to test algorithms on list of tickers...')
        for tickerCode in stockCSV:
            AlgoTester(tickerCode, True)


# Houses the framework for test mode
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


# Logs you into webull paper and houses framework for paper mode
def ModePaperTrade():
    global currentMode
    global userInput
    global pwb
    global availableMoney
    if currentMode != 'paper':
        print('Launching in paper trade mode...\n')
        print('Paper mode is a simulated trading mode (that works only with stocks and not crypto) run through Webull.')
        print('Though this mode does not trade with real money, it uses the same algo as Normal Trade mode.')
        print('-ls prints your account info and refreshes tracked tickers.')
        print('The command "watch" lets Beholder watch your portfolio and make trades.')
        print('Checking for WebullLogin.txt...')
        try:
            loginText = open('Info/WebullLogin.txt', 'r')
            loginInfo = loginText.readlines()
            print('WebullLogin.txt found!  Attempting to login...')
            pwb.login(username=loginInfo[0][0:len(loginInfo[0]) - 1], password=loginInfo[1])
            paperAccountInfo = pwb.get_account()
            print('Login Successful!')
            PrintAccountInfo(paperAccountInfo)
        except:
            notLogged = True
            while (notLogged):
                try:
                    loginInfo = ['', '']
                    print('Either WebullLogin.txt was not found or login failed.  Enter email manually: ', end='')
                    loginInfo[0] = input() + '\n'
                    print('Now enter password manually: ', end='')
                    loginInfo[1] = input()
                    pwb.login(username=loginInfo[0][0:len(loginInfo[0]) - 1], password=loginInfo[1])
                    paperAccountInfo = pwb.get_account()
                    PrintAccountInfo(paperAccountInfo)
                    notLogged = False
                except:
                    notLogged = True
    availableMoney = paperAccountInfo['accountMembers'][1]['value']
    currentMode = 'paper'
    while userInput != 'return' and userInput != 'exit':
        if userInput == 'watch':
            try:
                print('Beholder is watching:')
                try:
                    watchedTickers = open('Info/Paper/WatchList.txt')
                    watchedTickers = watchedTickers.readlines()
                    print(watchedTickers)
                    print('Press Ctrl^C to stop him...')
                    keepWatching = True
                except:
                    print('No holdings tracked so Beholder watches nothing.  Use the -add command.')
                    keepWatching = False
                while keepWatching:
                    Watch(watchedTickers)
            except:
                print('Closing his eyes...')
        print('BeholderCMD/PaperTrading: ', end='')
        userInput = input()
        ParseUserInput(userInput)
    print('Warning! Exiting paper trading mode.  This will stop Beholder from market watching until resumed...')
    currentMode = 'main'


# Logs you into webull and houses framework for normal mode
def ModeActualTrade():
    global currentMode
    global userInput
    global wb
    global availableMoney
    if currentMode != 'normal':
        print('Launching in actual trade mode...')
        print('WARNING!!! THIS MODE DEALS IN REAL MONEY! THE DEVELOPER IS NOT A FINANCIAL ADVISOR! USE AT OWN RISK!')
        print(
            'This mode functions almost identically to Paper mode (with same commands) except this mode allows the trading of Crypto Currency.')
        print("I highly recommend using paper mode until you are familiar with Beholder and it's commands")
        print('-ls prints your account info and refreshes tracked tickers.')
        print('The command "watch" lets Beholder watch your portfolio and make trades.')
        print('Checking for WebullLogin.txt... ')
        try:
            loginText = open('Info/WebullLogin.txt', 'r')
            loginInfo = loginText.readlines()
            print('WebullLogin.txt found!  Attempting to login...')
            wb.login(username=loginInfo[0][0:len(loginInfo[0]) - 1], password=loginInfo[1])
            NormalAccountInfo = wb.get_account()
            print('Login Successful!')
            PrintAccountInfo(NormalAccountInfo)
        except:
            notLogged = True
            while (notLogged):
                try:
                    loginInfo = ['', '']
                    print('Either WebullLogin.txt was not found or login failed.  Enter email manually: ', end='')
                    loginInfo[0] = input() + '\n'
                    print('Now enter password manually: ', end='')
                    loginInfo[1] = input()
                    wb.login(username=loginInfo[0][0:len(loginInfo[0]) - 1], password=loginInfo[1])
                    NormalAccountInfo = wb.get_account()
                    PrintAccountInfo(NormalAccountInfo)
                    notLogged = False
                except:
                    notLogged = True
    availableMoney = NormalAccountInfo['accountMembers'][1]['value']
    currentMode = 'normal'
    while userInput != 'return' and userInput != 'exit':
        if userInput == 'watch':
            try:
                print('Beholder is watching:')
                try:
                    watchedTickers = open('Info/Normal/WatchList.txt')
                    watchedTickers = watchedTickers.readlines()
                    print(watchedTickers)
                    print('Press Ctrl^C to stop him...')
                    keepWatching = True
                except:
                    print('No holdings tracked so Beholder watches nothing.  Use the -add command.')
                    keepWatching = False
                while keepWatching:
                    Watch(watchedTickers)
            except:
                print('Closing his eyes...')
        print('BeholderCMD/NormalTrading: ', end='')
        userInput = input()
        ParseUserInput(userInput)
    print('Warning! Exiting Normal trading mode.  This will stop Beholder from market watching until resumed...')
    currentMode = 'main'


# Runs ongoing
def Watch(watchedTickers):
    global currentMode
    global lastLook
    tempDay = datetime.date.today()
    if tempDay.day != lastLook.day:
        lastLook = tempDay
        GetData(watchedTickers, True)
        print('\nUpdated prices for:')
        print(watchedTickers)
        if currentMode == 'paper':
            x = 0
        elif currentMode == 'normal':
            x = 0


# Makes changes to the watched tickers lists
def WatchedTickerList(addOrRm, ticker, ):
    global currentMode
    global availableMoney
    hasTicker = False
    path = ''
    if currentMode == 'paper':
        try:
            path = 'Info/Paper/'
            watchListTXT = open(path + 'WatchList.txt', 'r')
            tickerListTXT = open(path + 'Tickers.txt', 'r')
        except:
            with open('Info/Paper/WatchList.txt', 'w') as output:
                output.write('')
            WatchedTickerList(addOrRm, ticker)
            return
    elif currentMode == 'normal':
        try:
            path = 'Info/Normal/'
            watchListTXT = open(path + 'WatchList.txt', 'r')
            tickerListTXT = open(path + 'Tickers.txt', 'r')
        except:
            with open('Info/Normal/WatchList.txt', 'w') as output:
                output.write('')
            WatchedTickerList(addOrRm, ticker)
            return
    with watchListTXT as WL:
        watchList = WL.readlines()
    with tickerListTXT as TL:
        tickerList = TL.readlines()
    if addOrRm == 'rm':
        for t in watchList:
            if t[len(t)-1:len(t)] == '\n':
                t = t[0:len(t)-1]
            if t == ticker:
                watchList.remove(t + '\n')
                print(ticker + ' was removed from ' + currentMode + ' watchlist')
                break
    elif addOrRm == 'add':
        for t in watchList:
            if t[len(t)-1:len(t)] == '\n':
                t = t[0:len(t)-1]
            if t == ticker:
                print(ticker + ' is already on' + currentMode + 'watchlist.')
                return
        for j in tickerList:
            if j[len(j)-1:len(j)] == '\n':
                j = j[0:len(j)-1]
            if j == ticker:
                hasTicker = True
                break
        if hasTicker:
            watchList.append(ticker + '\n')
            print(ticker + ' was added to' + currentMode + 'watchlist')
        else:
            print('Cannot add a ticker to watchlist that you do not own.')
            return
    else:
        print('addOrRm variable is not valid')
        return
    with open(path + 'WatchList.txt', 'w') as output:
        output.writelines(watchList)


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

while userInput != 'exit':
    print('BeholderCMD: ', end='')
    currentMode = 'menu'
    userInput = input()
    ParseUserInput(userInput)

print('\nGoodbye!')
sys.exit()