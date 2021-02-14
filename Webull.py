from webull import webull
from webull import paper_webull

wb = webull()
pwb = paper_webull()

print('Do you want to do "paper" or "normal" trading: ', end='')
tradingMode = input()
print('Looking for a file in /Info titled "WebullLogin.txt"...')
loginText = open('Info/WebullLogin.txt', 'r')
loginInfo = loginText.readlines()
# for line in loginInfo:
#     if line[len(line)-2:len(line)] == '\n':
#         print(line[0:len(line)-2])
#     else:
#         print(line)
if tradingMode == 'paper':
    print('Starting trading in paper mode...')
    pwb.login(username=loginInfo[0][0:len(loginInfo[0])-2], password=loginInfo[1])
elif tradingMode == 'normal':
    print('Starting trading with real money...')
    wb.login(username=loginInfo[0][0:len(loginInfo[0])-2], password=loginInfo[1])