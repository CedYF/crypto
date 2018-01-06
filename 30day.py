import pandas as pd
import numpy as np
import json
import requests
import urllib.request
from oauth2client.service_account import ServiceAccountCredentials
import gspread

#GSheets as Database
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet2 = client.open("ALTStats").worksheet('30day')
sheet = client.open("ALTStats").worksheet('Coins')

#GET COIN LIST
stats = sheet.col_values(17)
del stats[0]
coinlist = stats[:999]
print(coinlist)
day30 = []


#GET DATA 
for item in coinlist:
	try:
		url = urllib.request.urlopen("https://min-api.cryptocompare.com/data/histoday?fsym="+item+"&tsym=USD&limit=30").read().decode()
		Bitter = json.loads(url)
		df = json_normalize(Bitter['Data'])
		df2 = pd.DataFrame(df['close'])
		day30.append(item)
		for row in df2['close']:
			
			day30.append(row)
		print("Added"+item)
	except KeyError:
		print("mistakes happen: "+item+" take a look at this Ced")

#DECLARE CELLS TO BE UPDATED
x = 0
cell_list = sheet2.range('A2:AF1000')
for cell in cell_list:
    cell.value = day30[x]
    x = x + 1
    if x >= len(day30):
        break;

# Update in batch
sheet2.update_cells(cell_list)

