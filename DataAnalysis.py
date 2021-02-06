import sys
import pandas as pd
import matplotlib.pyplot as plt

isCrypto = False

print('This is the data analysis script.')
print('Provide link to csv file: ', end='')
dataFile = input()

#makes the data frame
try:
    dataParsed = pd.read_csv(dataFile, index_col='Date')
except:
    print('File name ' + dataFile + ' does not exist, make sure you included .csv at the end.')
    sys.exit()

# this if statement makes sure data sheet rows are in the right order, and reverses them if not
if pd.to_datetime(dataParsed.index[0]) > pd.to_datetime(dataParsed.index[len(dataParsed)-1]):
    newTemp = pd.DataFrame(dataParsed.iloc[::-1])
    dataParsed = newTemp

print(dataParsed)
print('Import Success!!!\n')

try:
    closePrice = dataParsed['Adj Close']
except:
    closePrice = dataParsed['close']
    isCrypto = True

# converts the date strings in the index into pandas datetime format
closePrice.index = pd.to_datetime(closePrice.index)
# closePrice.plot()
# plt.show()
print('\nPlease enter day number for SMAs from least to greatest:')
print('First num: ', end='')
tempSmaNum1 = int(input())
print('Second num: ', end='')
tempSmaNum2 = int(input())
print('Third num: ', end='')
tempSmaNum3 = int(input())

smaFirst = closePrice.rolling(window=tempSmaNum1).mean()
smaSecond = closePrice.rolling(window=tempSmaNum2).mean()
smaThird = closePrice.rolling(window=tempSmaNum3).mean()

#chart style
plt.style.use('dark_background')
#chart size
plt.figure(figsize=(12, 6))

#plotting price and SMA line in plt
plt.plot(closePrice, label='Adj Close', linewidth=2)
plt.plot(smaFirst, label=str(tempSmaNum1) + ' day rolling SMA', linewidth=1)
plt.plot(smaSecond, label=str(tempSmaNum2) + ' day rolling SMA', linewidth=2)
plt.plot(smaThird, label=str(tempSmaNum3) + ' day rolling SMA', linewidth=3)

#adds title and labels on the axes, making legend visible
plt.xlabel('Date')
plt.ylabel('Adjusted closing price ($)')
plt.title('Price with Simple Moving Average')
plt.legend()

plt.show()

# this processes the data into a data frame I can use
SMAPrice_df = pd.DataFrame({
    'Adj Close': closePrice,
    'SMA ' + str(tempSmaNum1): smaFirst,
    'SMA ' + str(tempSmaNum2): smaSecond,
    'SMA ' + str(tempSmaNum3): smaThird
})

SMAPrice_df.to_csv(dataFile[0:len(dataFile)-4] + '_SMA.csv')