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
closePrice.plot()
plt.show()

sma50 = closePrice.rolling(window=50).mean()
print(sma50)

#chart style
plt.style.use('dark_background')
#chart size
plt.figure(figsize=(12, 6))

#plotting price and SMA line in plt
plt.plot(closePrice, label='Adj Close', linewidth=2)
plt.plot(sma50, label='50 day rolling SMA', linewidth=1)

#adds title and labels on the axes, making legend visable
plt.xlabel('Date')
plt.ylabel('Adjusted closing price ($)')
plt.title('Price with a single Simple Moving Average')
plt.legend()

plt.show()