import bs4 as bs
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pickle 
import requests
import yfinance as yf

style.use('ggplot')

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

def visualize_data():
	#create correlation table
	df = pd.read_csv('sp500_joined_adjusted_closes.csv')
	df.set_index('Date', inplace=True)
	df_corr = df.corr()
	print(df_corr.head())
	#create color map for correlation matrix
	data = df_corr.values
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
	fig.colorbar(heatmap)
	ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
	ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
	ax.invert_yaxis()
	ax.xaxis.tick_top()
	column_labels = df_corr.columns
	row_labels = df_corr.index
	ax.set_xticklabels(column_labels)
	ax.set_yticklabels(row_labels)
	plt.xticks(rotation=90)
	heatmap.set_clim(-1, 1)
	plt.tight_layout()
	plt.show()

def visualize_data_2():
	#based on https://matplotlib.org/stable/users/explain/colors/colormap-manipulation.html#sphx-glr-users-explain-colors-colormap-manipulation-py
	#create correlation table
	df = pd.read_csv('sp500_joined_adjusted_closes.csv')
	df.set_index('Date', inplace=True)
	df_corr = df.corr()
	#print(df_corr.head())
	print(df_corr['ACN'])
	#create color map for correlation matrix
	data = df_corr.values
	viridis = mpl.colormaps['RdYlGn']
	n = len([viridis])
	fig, axs = plt.subplots(1, n, figsize=(n * 2 + 2, 3), layout='constrained', squeeze=False)
	for [ax, cmap] in zip(axs.flat, [viridis]):
		psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=-1, vmax=1)
		fig.colorbar(psm, ax=ax)
	column_labels = df_corr.columns
	row_labels = df_corr.index
	ax.set_xticklabels(column_labels)
	ax.set_yticklabels(row_labels)
	plt.show()


visualize_data()