import requests
import json
import collections
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('NASDAQ_API_KEY')
print(API_KEY)

r = requests.get('https://data.nasdaq.com/api/v3/datasets/FSE/AFX_X.json?api_key='+API_KEY)
print(r)
r.text

r = requests.get('https://data.nasdaq.com/api/v3/datasets/FSE/AFX_X/data.json?start_date=2017-01-01&end_date=2017-12-31&api_key='+API_KEY)
print(r)
dict = json.loads(r.text)

low = dict['dataset_data']['data'][0][3]
high = dict['dataset_data']['data'][0][2]
prev_close = dict['dataset_data']['data'][0][4]
max_change = 0
max_change_closing = 0 #between any two days. so calculate min/max closing prices
closing_low = dict['dataset_data']['data'][0][4]
closing_high = dict['dataset_data']['data'][0][4]
avg_vol = 0
total_trading_vol = 0
total_trade_days = 0

#columns are in this order (pulled from the json)
#"column_names": [
#	0		"Date",
#	1		"Open",
#	2		"High",
#	3		"Low",
#	4		"Close",
#	5		"Change",
#	6		"Traded Volume",
#	7		"Turnover",
#	8		"Last Price of the Day",
#	9		"Daily Traded Units",
#	10		"Daily Turnover"
#		],

for i in dict['dataset_data']['data']:
	#print("current: ", i)
	if i[3] <= low:
		low = i[3]
	if i[2] >= high:
		high = i[2]
		
	#calculate closing min/max
	if i[4] > closing_high:
		closing_high = i[4]
	if i[4] < closing_low:
		closing_low = i[4]
	
	#calculate intra day change based on high/low
	temp = abs(i[3] - i[2])
	if temp >= max_change:
		max_change = temp
	
	total_trading_vol = total_trading_vol + i[6]
	total_trade_days += 1
	
	
		
	
avg_vol = total_trading_vol / total_trade_days

print("lowest low : ", low)
print("highest high: ", high)
print("max day change: ", max_change)
print("max close change", abs(closing_high - closing_low))
print("avg trading vol", avg_vol)