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