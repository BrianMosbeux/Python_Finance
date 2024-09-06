import datetime as dt 
import matplotlib.pyplot as plt 
from matplotlib import style 
import pandas as pd 
import pandas_datareader.data as web
import yfinance as yf

start = dt.datetime(2000, 1, 1)
end = dt.datetime.today()
tickers = ['GOOG', 'TSLA']

def download_stocks_as_csv_files(stocks_tickers, start=dt.datetime(2000, 1, 1), end=dt.datetime.today()):
	for ticker in stocks_tickers:
		df = yf.download(ticker, start, end)
		df.to_csv(f'csv_stock_data/{ticker}.csv')


