from get_stock_data import get_sp500_data_from_yahoo, compile_adjusted_close_data
from machine_learning import extract_featuresets, do_machine_learning
from visualize_data import plot_historic_price_data_with_mplfinance
import pandas as pd
import pickle

#get_sp500_data_from_yahoo()
#compile_adjusted_close_data('20240912_stock_dfs')

ticker = 'AMZN'

X, y, df = extract_featuresets(ticker)
# confidence, classifier = do_machine_learning('AMZN')

#with open('{}clf.pickle'.format(ticker), 'wb') as f:
#	pickle.dump(classifier, f)

with open('{}clf.pickle'.format(ticker), 'rb') as f:
	clf = pickle.load(f)

print(df.tail())
print(clf.predict(X[-5:]))



amzn_df = pd.read_csv('20240912_stock_dfs/AMZN.csv', parse_dates=['Date'], index_col=['Date'])

plot_historic_price_data_with_mplfinance(amzn_df, ewmavs=[50, 100])