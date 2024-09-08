import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pickle 
import requests
import yfinance as yf

def save_sp500_tickers():
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = bs.BeautifulSoup(resp.text)
	table = soup.find('table', class_='wikitable sortable')
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		tickers.append(ticker.strip())
	with open('sp500tickers.pickle', 'wb') as f:
		pickle.dump(tickers, f)
	return tickers

def get_sp500_data_from_yahoo(reload_sp500=False):
	if reload_sp500:
		tickers = save_sp500_tickers()
	else:
		with open('sp500tickers.pickle', 'rb') as f:
			tickers = pickle.load(f)
	if not os.path.exists('stock_dfs'):
		os.makedirs('stock_dfs')
	start = dt.datetime(2000, 1, 1)
	end = dt.datetime.now()
	for ticker in tickers:
		print(ticker)
		if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
			df = yf.download(ticker, start, end)
			df.to_csv('stock_dfs/{}.csv'.format(ticker))
		else:
			print('Already have {}'.format(ticker))

def compile_adjusted_close_data():
	with open('sp500tickers.pickle', 'rb') as f:
		tickers = pickle.load(f)
	main_df = pd.DataFrame()
	for count, ticker in enumerate(tickers):
		df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
		df.set_index('Date', inplace=True)
		df.rename(columns={'Adj Close': ticker}, inplace=True)
		df.drop(labels=['Open', 'High', 'Low', 'Close', 'Volume'], axis=1, inplace=True)
		if main_df.empty:
			main_df = df
		else:
			main_df = main_df.join(other=df, on='Date', how='outer')
		if count % 10 == 0:
			print(count)
	print(main_df)
	main_df.to_csv('sp500_joined_adjusted_closes.csv')

compile_adjusted_close_data()