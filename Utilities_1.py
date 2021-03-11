# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 20:53:12 2021

@author: Yogesh
"""

import numpy as np
import pandas as pd
import os


import math
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA



def get_Residuals(pReturns,pFactorReturns):
    #storing the residuals
    lResiduals = pd.DataFrame(columns = pReturns.columns, index = pReturns.index)
    lCoef = pd.DataFrame(columns = pReturns.columns)
    ols = LinearRegression()
    for i in pReturns.columns:
        ols.fit(pFactorReturns, pReturns[i])
        lResiduals[i] = pReturns[i]-ols.intercept_-np.dot(pFactorReturns, ols.coef_)
        lCoef[i] = ols.coef_
    return lResiduals,lCoef




def get_sScore(pResiduals, kappa=252/30):
    lCumulativeResiduals = pd.DataFrame(pResiduals.cumsum())
    lCumulativeResiduals.index = lCumulativeResiduals.index.to_period('D')
    m = pd.Series(index = lCumulativeResiduals.index)
    sigma_eq = pd.Series(index = lCumulativeResiduals.columns)
    for i in lCumulativeResiduals.columns:
        lAR1Model = ARIMA(lCumulativeResiduals[i], order=(1,0,0))
        lAR1 = lAR1Model.fit()
        a = lAR1.params['const']
        b = lAR1.params['ar.L1']
        
        if -np.log(b) * 60 > kappa:
            tmp = (lCumulativeResiduals[i]-lCumulativeResiduals[i].shift(1)* b)[1:]
            a = tmp.mean()
            central_a =tmp - a
            m[i] = a/(1-b)
            sigma_eq[i]=math.sqrt(central_a.var()/(1-b*b))
    m = m.dropna()
    m = m - m.mean()
    Xt= lCumulativeResiduals.iloc[-1,:]
    sigma_eq = sigma_eq.dropna()
    s_score = (Xt-m)/sigma_eq
    return s_score


def get_Baskets(sScores,  sbo=1, sso=1, sbc=0.25, ssc=0.25):
    
    #### inputs
    SumOfWeightsL = 1
    SumOfWeightsS = 1
    sScores = sScores.replace([np.inf, -np.inf], np.nan)
    sScores.dropna(inplace=True)
    sScoresL = sScores[sScores<-sbo]
    sScoresS = sScores[sScores>-sso]
    # equal weight implementation
    nStocksL = len(sScoresL) 
    nStocksS = len(sScoresS)
    
    WeightsL = pd.Series(index=sScoresL.index, dtype='float64')
    WeightsL.fillna(SumOfWeightsL/nStocksL, inplace=True)
    WeightsS = pd.Series(index=sScoresS.index)
    WeightsS.fillna(-SumOfWeightsS/nStocksS, inplace=True)
    lWeights = WeightsL.append(WeightsS)
    return(lWeights)
        
def get_PortfolioReturn(pWeights, pDailyReturns, pRebalancingFrequency, pTxnCost=0):
    
    lRelevantTickers = [c for c in pDailyReturns.index if c in pWeights.index]
    lDailyReturns = pDailyReturns[lRelevantTickers]
    lPortfolioReturns = lDailyReturns@pWeights
    #lCumulativeReturns = (lPortfolioReturns+1).cumprod()
    return(lPortfolioReturns)
    
    
    
    
    
    
    
    
    
    
    
    
    
    