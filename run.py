
import pandas as pd

def process_data_for_labels(ticker):
	how_many_days = 7
	df = pd.read_csv('sp500_joined_adjusted_closes.csv', index_col=0)
	tickers = df.columns.values
	df.fillna(0, inplace=True)

	for i in range(1, how_many_days+1):
		df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
	df.fillna(0, inplace=True)
	return tickers, df

def buy_sell_hold(*args):
	cols = [c for c in args]
	requirement = 0.02
	for col in cols:
		if col > requirement:
			return 1
		if col < -requirement:
			return -1
	return 0