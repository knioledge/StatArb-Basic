# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 16:15:32 2021

@author: Yogesh
"""

import numpy as np
import pandas as pd
import os
os.chdir("D://Work//Projects//StatArb//")
import pickle
# load the data from csv
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from scipy.stats import mstats
import Utilities_1
from Utilities_1 import *
import warnings

tRawData = pickle.load(open("t_data_2.pkl", "rb"))

tRawData.head()

tRawData_close = tRawData.pivot(columns='Ticker', values='Close')
tRawData_returns = tRawData_close.pct_change(1)
tRawData_returns.fillna(0, inplace=True)


# Generate windowed tables
window = 120
resi = {}
pResults = {}
pcaresults = {}

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    
for t in np.arange(len(tRawData_returns.index)- window):
    tRawDataWindow = tRawData_returns[(0 + t):(window+t)]
    try:
        tReturnDate = tRawData_returns.iloc[window+t+1].name
    except:
        print("reached end of loop")
    
    tRawDataWindow_scaled = pd.DataFrame(StandardScaler().fit_transform(tRawDataWindow), columns=tRawDataWindow.columns, index=tRawDataWindow.index)        
    tRawDataWindow_scaled.fillna(0, inplace=True)
    
    tcorrmat = tRawDataWindow_scaled.corr()
    
# do PCA and get the eigenvectors and eigenportfolio returns
    pca = PCA(n_components=15)
    weights = pd.DataFrame(pca.fit_transform(tcorrmat.fillna(0)), index=tRawDataWindow_scaled.columns)
    pcareturn = pd.DataFrame(np.dot(tRawDataWindow_scaled, weights))
    pcaresults[t] = pcareturn
    resi[t] = get_Residuals(tRawDataWindow_scaled, pcareturn)[0]
    
    print("Loop " + str(t + 1) + " of " + str(len(tRawData_returns.index) - window ) + " done!")
    pScores = get_sScore(resi[t])
    try:
        pBaskets = get_Baskets(pScores)
    except:
        print("No stocks found in this iteration. Using last date's weights")
    pPortfolioReturns = get_PortfolioReturn(pBaskets,tRawData_returns.loc[tReturnDate],1)
    pResults[tReturnDate] = pPortfolioReturns
    print("the results for date " + str(tReturnDate) + " is " + str(pResults[tReturnDate]))
    
    
pResults_ts = pd.DataFrame(pResults.items(), columns=['Date_', 'Returns'])
pResults_ts.set_index('Date_', inplace=True)
(pResults_ts+1).cumprod().plot()