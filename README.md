# StatArb-Basic
 Basic implementation of a version of the paper by Avellaneda
 
 Features:
 
 - Data from Yahoo Finance ( need to upgrade to IBKR data feeds )
 - Equal weighted portfolio  ( need to implement an optimized portfolio)
 - Using previous day closing prices ( need to use previous day vwap prices and assume mid-day execution )
 - No transaction costs ( need to include txn cost curves )
 - Uses a for loop to loop through windows ( Need a better algorithm that can parallelize some operations )
 - Currently using PCA factors ( Need to expand using industry factors and custom risk models )
 - Universe is a measly 120ish EM stocks ( Need to expand to a much broader universe )
 - Currently having some survivorship bias due to selection of stocks in the universe from the current MSCI EM index ( broader point in time universe needs to be used )
 - No fundamental factors used ( Need to incorporate investment styles into the residual calculation model )
 - Using an OU process to model the mean reversion ( Need to use more advanced models that do not assume Gaussian properties ) 
 - Maximum Likelihood estimation currently for the OU process parameters. ( need to explore state space models for parameter estimation , example Kalman filters or other frequency domain methods) 
 - Shorting is assumed to be frictionless. (Need to incorporate market volatility based shorting costs)
 - Sell/Buy triggers and other parameter estimates are based on heuristics (Need to have a data dependent way such as a cross validation set )
 - Currently using linear regression to calculate residuals. (Perhaps need to capture some nonlinearities to make the process truly stationary)
 - Need to impose real world constraints in the optimization / rebalncing process such as Sector / Country / Macro risk constraints
 
 
