
from collections import Counter
import numpy as np
import pandas as pd

def process_data_for_labels(ticker):
	how_many_days = 7
	df = pd.read_csv('sp500_joined_adjusted_closes.csv', index_col=0)
	tickers = df.columns.values
	df.fillna(0, inplace=True)

	for i in range(1, how_many_days+1):
		df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
	df.fillna(0, inplace=True)
	return how_many_days, tickers, df

def buy_sell_hold(*args):
	cols = [c for c in args]
	requirement = 0.02
	for col in cols:
		if col > requirement:
			return 1
		if col < -requirement:
			return -1
	return 0

def extract_featuresets(ticker):
	how_many_days, tickers, df = process_data_for_labels(ticker)
	df['{}_target'.format(ticker)] = list(map(buy_sell_hold, *[df['{}_{}d'.format(ticker,i)] for i in range(1,how_many_days+1)]))
	vals = df['{}_target'.format(ticker)].values
	str_vals = [str(i) for i in vals]
	print('Data spread', Counter(str_vals))
	df.fillna(0, inplace=True)
	df = df.replace([np.inf, -np.inf], np.nan)
	df.dropna(inplace=True)
	df_vals = df[[ticker for ticker in tickers]].pct_change()
	df_vals = df_vals.replace([np.inf, -np.inf], 0)
	df_vals.fillna(0, inplace=True)
	X = df_vals.values 
	y = vals
	return X, y, df