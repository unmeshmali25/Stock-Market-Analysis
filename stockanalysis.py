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


# Exploring pairplots
sns.pairplot(tech_rets.dropna())




#Analysing risk vs expected returns
rets = tech_rets.dropna()

area = np.pi*20

plt.scatter(rets.mean(), rets.std(), s = area)

plt.xlabel('Expected return')
plt.ylabel('Risk')

for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
    plt.annotate(
    label,
    xy = (x,y), xytext = (50,50),
    textcoords = 'offset points', ha = 'right', va = 'bottom', 
    arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3, rad = -0.3'))



# Value at risk using the "Bootstap" method
rets['AAPL'].quantile(0.05)
# The value of this will determine 95% confidence on profit/loss percent



# Value at risk using Monte Carlo method
days = 365
dt = 1/days
mu = rets.mean()['GOOG']
sigma = rets.std()['GOOG']

def stock_monte_carlo(start_price, days, mu, sigma):
    price = np.zeros(days)
    price[0] = start_price
    
    shock = np.zeros(days)
    drift = np.zeros(days)
    
    for x in xrange(1,days):
        shock[x] = np.random.normal(loc = mu.dt, scale = sigma.np.sqrt(dt))
        drift[x] = mu.dt
        price[x] = price[x-1] + (price[x-1]*(drift[x] + shock[x]))
        
    return price

start_price = 1205.02
for run in range(100):
    plt.plot(stock_monte_carlo(start_price, days, mu, sigma))

