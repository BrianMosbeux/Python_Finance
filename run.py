import datetime as dt 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
from matplotlib import style 
import mplfinance as mpf
import pandas as pd 
#from pandas_datareader import data as web
import yfinance as yf


#style.use('ggplot')

start = dt.datetime(2000, 1, 1)
end = dt.datetime.today()
tickers = ['GOOG', 'TSLA']

def download_stocks_as_csv_files(stocks_tickers, start=dt.datetime(2000, 1, 1), end=dt.datetime.today()):
	for ticker in stocks_tickers:
		df = yf.download(ticker, start, end)
		df.to_csv(f'csv_stock_data/{ticker}.csv')

def plot_historic_price_data_with_pandas_and_mpl(df):
	df['50ma'] = df['Adj Close'].rolling(window=50).mean()
	df['100ma'] = df['Adj Close'].rolling(window=100).mean()
	df[['Adj Close', '100ma', '50ma']].plot()
	plt.show()
	#plt.savefig('figure.png')

def plot_historic_price_data_with_mpl(df):
	#add moving averages to dataframe
	df['50ma'] = df['Adj Close'].rolling(window=50).mean()
	df['100ma'] = df['Adj Close'].rolling(window=100).mean()
	# create sublots
	ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
	ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
	# add data and labels to subplot
	ax1.plot(df.index, df['Adj Close'], label='Adj Close')
	ax1.plot(df.index, df['100ma'], label='100ma')
	ax1.plot(df.index, df['50ma'], label='50ma')
	ax2.bar(df.index, df['Volume'])
	ax1.legend()
	ax1.set_ylabel('price per share')
	ax2.set_ylabel('volume')
	plt.show()

# mavs is the list of moving averages you want to display on graph
# mavs=[50,100] would calculate the moving average on a 50 period window and a 100 period window
# ewmavs is the list of exponentially weighted moving average you want to display on graph using pandas.DataFrame.ewm (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)
# mavs=[50,100] would calculate the exponentially weighted moving average on a 50 period span and a 100 period span
def plot_historic_price_data_with_mplfinance(df, mavs=[], ewmavs=[], volume=True, macd=True):
	add_plot_list = [] 
	# caluclate moving average
	for ma in mavs: 
		plot_line = df['Adj Close'].rolling(window=ma).mean()
		add_plot_list.append(mpf.make_addplot(plot_line, label=f'ma{ma}'))
	for ema in ewmavs:
		plot_line = df['Adj Close'].ewm(span=ema, adjust=False).mean()
		add_plot_list.append(mpf.make_addplot(plot_line, label=f'ema{ema}'))
	if macd:
		exp12 = df['Adj Close'].ewm(span=12, adjust=False).mean()
		exp26 = df['Adj Close'].ewm(span=26, adjust=False).mean()
		macd = exp12 - exp26
		signal = macd.ewm(span=9, adjust=False).mean()
		hist = macd - signal
		macd_plot_list = [
			mpf.make_addplot(hist,type='bar',width=0.6,panel=1,color='dimgray',alpha=1),
			mpf.make_addplot(macd,panel=1,color='#ad6eff', label='macd', ylabel='macd',secondary_y=True,y_on_right=False),
			mpf.make_addplot(signal,panel=1,color='#ffa33f', label='signal',secondary_y=True)
			]
		add_plot_list += macd_plot_list

	mpf.plot(df, type='candle', volume=True, volume_panel=2, style='charles', addplot=add_plot_list)


#df = pd.read_csv('csv_stock_data/GOOG.csv', parse_dates=True, index_col=0)
#df = df.loc['2024-06-01':end,:]

#plot_historic_price_data_with_pandas_and_mpl(df)
#plot_historic_price_data_with_mpl(df)
#plot_historic_price_data_with_mplfinance(df, ewmavs=[50, 200])

