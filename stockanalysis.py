import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import seaborn as sns
import scipy as stats

from pandas_datareader import DataReader
from datetime import datetime

# To take care of floating numbers
from __future__ import division

tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

end = datetime.now()
start = datetime(end.year - 1, end.month, end.day)

# To create data frame for each of the stock tickers
for stock in tech_list:
    globals()[stock] = DataReader(stock, 'yahoo', start, end)

 # Plotting the adjusted closing price over the entire year
 AAPL['Adj Close'].plot(legend = True, figsize = (10,4))

 # Plotting daily volume traded
AAPL['Volume'].plot(legend = True, figsize = (10,4))

# Calculating and plotting moving average
ma_day = [10,20,50]
for ma in ma_day:
    column_name = 'MA for %s days'%(str(ma))
    
    AAPL[column_name] = AAPL['Adj Close'].rolling(ma).mean()
    

AAPL[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(legend = True, figsize = (10,4))


# Finding daily return -- Percent change of the adjusted close column
AAPL['Daily return'] = AAPL['Adj Close'].pct_change()
AAPL['Daily return'].plot(legend = True, figsize = (10,4), linestyle = '--', marker = 'o')

# Plotting histogram and kde plot together
sns.distplot(AAPL['Daily return'].dropna(), bins = 100, color = 'yellow')



#Analysing returns on all the stocks in the list
closing_df = DataReader(tech_list, 'yahoo', start, end)['Adj Close']
tech_rets = closing_df.pct_change()

# Comparing 2 stocks with each other
sns.jointplot('AAPL','GOOG', tech_rets,  kind = 'scatter', color = 'green')



