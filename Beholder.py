# This is the master beholder script
# Eventually this is the program you will run and all the features from other testing scripts will be implemented
#
# This bot and supplementary explanatory .py scripts where done by Tamblin Papendorp

import sys
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import math
from datetime import datetime
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
        elif inputStr.isupper():
            GetData(inputStr)
        else:
            print('Not a valid command. Refer to readme on how to use test mode. type return to go back to menu')
    else:
        print('Not a valid command.')


def GetData(tickerCode):
    print('Attempting to get historical data for ' + tickerCode + '...')
    stock = yf.download(tickers=tickerCode, period='MAX')
    if len(stock) < 0:
        print("\nNot a stock, trying crypto...")
        stock = yf.download(tickers=tickerCode + "-USD", period='MAX')
    if len(stock) > 1:
        print('Data for ' + tickerCode + ' found and imported!\n')
        stock.to_csv('Data/' + tickerCode + '_stats.csv')
    else:
        print('Not a valid ticker for stock/crypto\n')


def AlgoTester(dataFrame, algo, stockName):
    print('Preparing to test algorithm ' + algo + ' on ' + stockName + '...')


def ModeTest():
    global currentMode
    global userInput
    if currentMode != 'test':
        print('Launching in test mode...\n')
        print('Test mode is used mainly for testing the effectiveness of Beholder and its eyes on past data.')
        print('Test mode will run a simulation on all historical data available of a certain stock or crypto.')
        print('Enter ticker info for holding you would like to track.\n')
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
