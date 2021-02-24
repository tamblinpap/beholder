# beholder
Stock/Crypto trend analysis 

This bot is currently in development and is not ready to use.
Beholder.py is the main bot, and the other .py files are the different functionalities split for ease of understanding how the bot works.
If you are having any unintended bugs or have suggestions email me at tamblinpap@gmail.com

# Implemented Functions
-m test mode is ready to use
-m normal and -m paper are not finished but can display account information and run tests on holdings

# Test Mode
Test mode pulls all data available form yahoo finance and checks my algorithm against it.
- the '-g' command gets data in the form of a csv file and stores it in the /Data/ folder
- the '-ls' command lists all the csv files you have available
- the '-t' command tests the algo over the course of a csv files history for 10 day SMA's, WMA's, and EMA's against 25 day and 100 day SMA's
  -(I plan to implement more complex algo's or test for optimal moving averages later)

# Normal/Paper Trading Mode
When launching normal or paper trading mode you can log in automatically by having a WebullLogin.txt file
in the info folder with your email on the first line and your password on the second.  Or you can input them
manually everytime you enter the mode.  These modes are not finished.