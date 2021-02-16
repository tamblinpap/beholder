from webull import webull
from webull import paper_webull

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
if tradingMode == 'paper':
    print('Starting trading in paper mode...')
    pwb.login(username=loginInfo[0][0:len(loginInfo[0])-1], password=loginInfo[1])
    try:
        pwb.get_account_id()
        print('Login successful!')
        print(pwb.get_account())
    except:
        print('Login unsuccessful.  Check login info.')

elif tradingMode == 'normal':
    print('Starting trading with real money...')
    wb.login(username=loginInfo[0][0:len(loginInfo[0])-1], password=loginInfo[1])
    try:
        wb.get_account_id()
        print('Login successful!')
        print(wb.get_account())
    except:
        print('Login unsuccessful.  Check login info.')