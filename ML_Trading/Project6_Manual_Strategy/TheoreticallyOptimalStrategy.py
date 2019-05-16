# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 21:52:07 2019

@author: Deepika

"""
"""
TheoreticallyOptimalStrategy.py Code implementing a TheoreticallyOptimalStrategy object (details below). It should implement testPolicy() which returns a trades data frame (see below). The main part of this code should call marketsimcode as necessary to generate the plots used in the report.
"""
import datetime as dt 
import pandas as pd
import marketsimcode as msim
from util import get_data, plot_data

class TheoreticallyOptimalStrategy(object):

    def __init__(self):
        pass # move along

    def author():
        return 'dsivakumar6'

    def testPolicy(self,symbol = "JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        # Get the symbol in a list
        symbols = []
        symbols.append(symbol)
        # Get the date range
        dates = pd.date_range(sd, ed)
        # Get all the prices of the symbols
        price_all = get_data(symbols, dates)  # automatically adds SPY
        # Forward fill and Backward fill
        price_all = price_all.fillna(method='ffill')
        price_all = price_all.fillna(method='bfill')
        price = price_all[symbols]  # only portfolio symbols 

         # Create the df_trades dataframe
        df_trades = price.copy()
        # Clear out the Dataframe so we can accumulate values into it
        for day in range(price.shape[0]):
            for sym in symbols:
                df_trades.ix[day,sym] = 0.0
        # Holdings for each symbol (At any given day, the holdings should be only be either -1000, 0 or 1000)
        holdings = {sym:0 for sym in symbols}

        # Iterate through the dataframe to add trades
        for day in range(price.shape[0]-1):
            for sym in symbols:
                if sym == 'SPY':
                    continue
                today_price = price.ix[day,sym]
                tomorrow_price = price.ix[day+1,sym]
                if (tomorrow_price > today_price) and (holdings[sym] < 1000):
                    # BUY 1000 shares first
                    df_trades.ix[day,sym] = 1000.0
                    holdings[sym] = holdings[sym] + 1000
                    # Even then, if the holdings sums upto only 0, BUY a 1000 more shares
                    if (holdings[sym] == 0):
                        df_trades.ix[day,sym] = df_trades.ix[day,sym] + 1000
                        holdings[sym] = holdings[sym] + 1000
                elif (tomorrow_price < today_price) and (holdings[sym] > -1000):
                    # SELL 1000 shares first
                    df_trades.ix[day,sym] = -1000.0
                    holdings[sym] = holdings[sym] - 1000
                    # Even then, if the holdings comes to only 0, SELL a 1000 more shares
                    if (holdings[sym] == 0):
                        df_trades.ix[day,sym] = df_trades.ix[day,sym] - 1000
                        holdings[sym] = holdings[sym] - 1000
        return df_trades

    # Calculate the Benchmark using JPM
    def benchmark(self,sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
        # Get the date range
        dates = pd.date_range(sd, ed)
        # Get the symbol in a list
        symbols = []
        symbols.append("JPM")
         # Get all the prices of the symbols
        price_all = get_data(symbols, dates)  # automatically adds SPY
        # Forward fill and Backward fill
        price_all = price_all.fillna(method='ffill')
        price_all = price_all.fillna(method='bfill')
        # Get only the JPM price
        price_JPM = price_all[symbols]

        # Create the df_trades dataframe
        df_trades = price_JPM.copy()
        # Clear out the Dataframe so we can accumulate values into it
        for day in range(df_trades.shape[0]):
            for sym in symbols:
                df_trades.ix[day,sym] = 0.0
        # Investing in 1000 shares of JPM and holding that position.
        df_trades.iloc[0] = +1000
        return df_trades

if __name__ == "__main__": 
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    sv = 100000
    commission=0.00
    impact=0.0

    tos = TheoreticallyOptimalStrategy()
    # Calculate trades using Theoritically optimal strategy
    df_trades = tos.testPolicy(symbol = "JPM", sd=sd, ed=ed, sv=sv)
    # Calculate Long(BUY) & Short(SELL) entries seperately for plotting vertical lines
    long_trades = df_trades[df_trades > 0]
    long_trades = long_trades.dropna()
    short_trades = df_trades[df_trades < 0]
    short_trades = short_trades.dropna()
    # Calculate trades for the benchmark
    df_trades_benchmark = tos.benchmark(sd=sd, ed=ed, sv=sv)

    # Compute the Theoritically optimal Portfolio value
    df_portvals = msim.compute_portvals(df_trades, start_val=sv, commission=commission, impact=impact)

#    print('***************************df_portvals***************************')
#    print(df_portvals)
    # Compute the Benchmark Portfolio value
    df_portvals_benchmark = msim.compute_portvals(df_trades_benchmark, start_val=sv, commission=commission, impact=impact)

    # Normalize the values
    normed_portvals = df_portvals / df_portvals.values[0]
    normed_portvals_benchmark = df_portvals_benchmark / df_portvals_benchmark.values[0]

    tos_df = pd.concat([normed_portvals_benchmark, normed_portvals], axis=1)
    tos_df.columns = ['Benchmark','Portfolio']
    ax_tos = tos_df.plot(title="Theoritically Optimal Strategy", fontsize=12, linewidth=1, grid=True, color=['C2','Red'])
    ax_tos.set_xlabel("Date")
    ax_tos.set_ylabel("Portfolio Value")
    plt.legend()
#    plt.savefig("tos.png")
#    plt.close()
    plt.show()

    # Compute Portfolio statistics
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = msim.compute_stats(df_portvals)
    # Compute Benchmark statistics
    cum_ret_benchmark, avg_daily_ret_benchmark, std_daily_ret_benchmark, sharpe_ratio_benchmark = msim.compute_stats(df_portvals_benchmark)
    # Compare portfolio against Benchmark
    print "******************Theoritically Optimal Strategy Results*******************"
    print "Date Range: {} to {}".format(sd, ed) 
    print 
    print "Sharpe Ratio of Portfolio: {}".format(sharpe_ratio) 
    print "Sharpe Ratio of Benchmark : {}".format(sharpe_ratio_benchmark) 
    print 
    print "Cumulative Return of Portfolio: {}".format(cum_ret) 
    print "Cumulative Return of Benchmark : {}".format(cum_ret_benchmark) 
    print 
    print "Standard Deviation of Portfolio: {}".format(std_daily_ret) 
    print "Standard Deviation of Benchmark : {}".format(std_daily_ret_benchmark) 
    print 
    print "Mean of Daily Returns of Portfolio: {}".format(avg_daily_ret) 
    print "Mean of Daily Returns of Benchmark : {}".format(avg_daily_ret_benchmark) 
    print 
    print "Final Portfolio Value: {}".format(df_portvals[-1]) 
    print "Final Benchmark Value: {}".format(df_portvals_benchmark[-1]) 