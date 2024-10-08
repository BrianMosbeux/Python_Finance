import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pickle
import requests
import yfinance as yf


def save_sp500_tickers():
	resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
	soup = bs.BeautifulSoup(resp.text, 'lxml')
	table = soup.find('table', class_='wikitable sortable')
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		tickers.append(ticker.strip())
	with open('sp500tickers.pickle', 'wb') as f:
		pickle.dump(tickers, f)
	return tickers

def download_stocks_as_csv_files(tickers, output_folder, start=dt.datetime(2000, 1, 1), end=dt.datetime.today()):
	for ticker in tickers:
		print(ticker)
		if not os.path.exists('{}/{}.csv'.format(output_folder, ticker)):
			df = yf.download(ticker, start, end)
			df.to_csv('{}/{}.csv'.format(output_folder, ticker))
		else:
			print('Already have {}'.format(ticker))

def get_sp500_data_from_yahoo(reload_sp500=False):
	start = dt.datetime(2000, 1, 1)
	end = dt.datetime.now()
	date_string = end.strftime('%Y%m%d')
	output_folder = '{}_stock_dfs'.format(date_string)
	if reload_sp500:
		tickers = save_sp500_tickers()
	else:
		with open('sp500tickers.pickle', 'rb') as f:
			tickers = pickle.load(f)
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	download_stocks_as_csv_files(tickers=tickers, start=start, end=end, output_folder=output_folder)

def compile_adjusted_close_data(input_folder):
	with open('sp500tickers.pickle', 'rb') as f:
		tickers = pickle.load(f)
	main_df = pd.DataFrame()
	for count, ticker in enumerate(tickers):
		df = pd.read_csv('{}/{}.csv'.format(input_folder, ticker))
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
