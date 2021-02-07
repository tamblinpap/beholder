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

userInput = ''


def SaveAsCSV(dataFrame):
    dataFrame.to_csv('Data/' + dataFrame + '.csv')


def ParseUserInput(input):
    if input == 'exit':
        return


def GetData(tickerCode):
    print('Getting historical data for ' + tickerCode + '...')


def AlgoTester(dataFrame, algo, stockName):
    print('Preparing to test algorithm ' + algo + ' on ' + stockName + '...')


def ModeTest():
    print('Launching in test mode...')


def ModePaperTrade():
    print('Launching in paper trade mode...')


def ModeActualTrade():
    print('Launching in actual trade mode...')


# Starting user interaction
beholderText = open('Data\Beholder.txt')
for element in beholderText:
    print(element)
print('Welcome to the "Beholder" bot!\n')
print('Please refer to the README.md file for operation instructions')
print('\nThe creator of this bot is not liable for any losses or data theft that may happen as a result of this bot')
print('The creator of this bot is not a financial advisor.  Use at your own risk')
print('Beholder Bot was created by Tamblin Papendorp')
print('\nWhat mode to you want to launch Beholder in?')

while userInput != 'exit':
    print('BeholderCMD: ', end='')
    userInput = input()
    ParseUserInput(userInput)

print('\nGoodbye!')
sys.exit()
