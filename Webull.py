from webull import webull
from webull import paper_webull
import pandas as pd
import sys

wb = webull()
pwb = paper_webull()
tradingMode = ''

while tradingMode != 'paper' and tradingMode != 'normal':
    if tradingMode != '':
        print('Not a valid mode, please type "paper" or "normal".')
    print('Do you want to do "paper" or "normal" trading: ', end='')
    tradingMode = input()

print('Looking for a file in /Info titled "WebullLogin.txt"...\n')
try:
    loginText = open('Info/WebullLogin.txt', 'r')
    loginInfo = loginText.readlines()
    print('WebullLogin.txt found and read!')
except:
    loginInfo = ['', '']
    print('No login text file found.  Enter username manually: ', end='')
    loginInfo[0] = input()+'\n'
    print('Now enter password manually: ', end='')
    loginInfo[1] = input()
# This statement tests the parsing of the strings
# for line in loginInfo:
#     if line[len(line)-2:len(line)] == '\n':
#         print(line[0:len(line)-2])
#     else:
#         print(line)

def PrintAccountInfo(accountInfo):
    print('\n\nACCOUNT INFO')
    try:
        print('Account type: ' + accountInfo['accounts'][0]['paperName'])
        isPaper = True
    except:
        print('Account type: Real ' + accountInfo['currency'])
        isPaper = False
    print('Total Account Value: ' + accountInfo['netLiquidation'])
    print('-(' + str(round(float(accountInfo['accountMembers'][1]['value'])/float(accountInfo['netLiquidation'])*100, 1)) + '%) Money in cash: ' + accountInfo['accountMembers'][1]['value'])
    print('-(' + str(round(float(accountInfo['accountMembers'][0]['value'])/float(accountInfo['netLiquidation'])*100, 1)) + '%) Money in holdings: ' + accountInfo['accountMembers'][0]['value'])
    if isPaper:
        for i in accountInfo['positions']:
            print('   >(' + str(round((float(i['marketValue'])/float(accountInfo['accountMembers'][0]['value']))*100, 1)) + '%) ' + str(i['position']) + ' share(s) of ' + i['ticker']['symbol'] + ' at $' + i['lastPrice'] + ' each')
    else:
        for i in accountInfo['positions']:
            if i['assetType'] == 'stock':
                print('   >(' + str(round((float(i['marketValue'])/float(accountInfo['accountMembers'][0]['value']))*100, 1)) + '%) ' + str(i['position']) + ' share(s) of ' + i['ticker']['symbol'] + ' at $' + i['lastPrice'] + ' each')
            elif i['assetType'] == 'crypto':
                print('   >(' + str(round((float(i['marketValue'])/float(accountInfo['accountMembers'][0]['value']))*100, 1)) + '%) ' + str(i['position']) + ' ' + i['ticker']['symbol'] + ' at $' + i['marketValue'])
    if accountInfo['openOrderSize'] > 0:
        print('Open Orders:')
        for i in accountInfo['openOrders']:
            try:
                print('   >' + i['action'] + 'ING ' + str(round(float(i['totalQuantity'])-float(i['filledQuantity']))) + ' of ' + i['totalQuantity'] + ' of ' + i['ticker']['tinyName'] + '(' + i['ticker']['symbol'] + ') for $' + i['lmtPrice'] + ' a share.')
            except:
                print('   >' + i['action'] + 'ING ' + str(round(float(i['totalQuantity'])-float(i['filledQuantity']))) + ' of ' + i['totalQuantity'] + ' of ' + i['ticker']['tinyName'] + '(' + i['ticker']['symbol'] + ') for market price')

    else:
        print('No Open Orders.')


if tradingMode == 'paper':
    print('Starting trading in paper mode...')
    pwb.login(username=loginInfo[0][0:len(loginInfo[0])-1], password=loginInfo[1])
    try:
        pwb.get_account_id()
        print('Login successful! Printing paper account information:\n')
        paperAccountInfo = pwb.get_account()
        for element in paperAccountInfo:
            print(element + ': ', end='')
            if type(paperAccountInfo[element]) == type(loginInfo):
                for subElement in paperAccountInfo[element]:
                    print('-', end='')
                    print(subElement)
            else:
                print(paperAccountInfo[element])
    except:
        print('Login unsuccessful.  Check login info.')
        sys.exit()
    PrintAccountInfo(paperAccountInfo)
    pwb.get_account_id()
    pwb.get_trade_token()
    pwb.place_order(stock='PLUG', action='SELL', quant=1, orderType='MKT', enforce='DAY')
    PrintAccountInfo(pwb.get_account())


elif tradingMode == 'normal':
    print('Starting trading with real money...')
    wb.login(username=loginInfo[0][0:len(loginInfo[0])-1], password=loginInfo[1])
    try:
        wb.get_account_id()
        print('Login successful! Printing account information:\n')
        realAccountInfo = wb.get_account()
        for element in realAccountInfo:
            print(element + ': ', end='')
            if type(realAccountInfo[element]) == type(loginInfo):
                for subElement in realAccountInfo[element]:
                    print('-', end='')
                    print(subElement)
            else:
                print(realAccountInfo[element])
    except:
        print('Login unsuccessful.  Check login info.')
        sys.exit()
    PrintAccountInfo(realAccountInfo)

userInput = ''

while userInput != 'exit':
    if tradingMode == 'paper':
        print('\nWebull Paper Trading: ', end='')
        userInput = input()
        if userInput == 'trade':
            print('What is the ticker for the stock you want to buy: ', end='')
            ticker = input()
            print('How many to do you to buy at market price of ' + str(pwb.get_ticker(ticker)) + ': ')
            amount = input()
            PrintAccountInfo(pwb.get_account())
    elif tradingMode == 'normal':
        print('\nWebull Real Trading: ', end='')
        userInput = input()