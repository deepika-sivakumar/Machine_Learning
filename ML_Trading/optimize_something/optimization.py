"""MC1-P2: Optimize a portfolio.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Deepika Sivakumar
GT User ID: dsivakumar6
GT ID: 903450354
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt 
from util import get_data, plot_data
import scipy.optimize as spo

#Function for the minimizer
def f(allocs_guess, normed, start_value):
    alloced = normed * allocs_guess
    pos_value = alloced * start_value
    port_value = pos_value.sum(axis=1)
    daily_rets = compute_daily_returns(port_value)
#    cr = (port_value[-1]/port_value[0]) - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sharpe_ratio=  adr/sddr
    sr= np.sqrt(252)*sharpe_ratio
    sr = sr * -1
    return sr

#Function to Compute the daily returns
def compute_daily_returns(port_value):
    daily_returns = port_value.copy()
    daily_returns[1:] =(port_value[1:]/port_value[:-1]) - 1
    daily_returns = daily_returns[1:]
    return daily_returns

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY

    prices = prices_all[syms]  # only portfolio symbolsde32 
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    
    ## Calculate Sample Allocation
#    allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations
    
    #Starting Value of funds allocated to the portfolio
    start_value = 100000
    #Calculate the total no. of stocks in the portfolio
    no_of_stocks = len(syms)
    #Formulate an uniform allocation of stocks as the initial guess
    allocs_guess = [1.0/no_of_stocks] * no_of_stocks
    
#    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats

    # Calculate the normalised value
    normed = prices/prices.values[0]

    # Define the bounds for the allocation values for the minimizer function
    allocs_bounds = [(0.0,1.0)]
    for i in range(no_of_stocks-1):
        allocs_bounds.append((0.0,1.0))

    # Define the constraints for the allocation values for the minimizer function
    alloc_constraints=({ 'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs) })

    normed = np.asarray(normed)

    # Call the scipy minimizer function
    min_result = spo.minimize(f, allocs_guess, args=(normed,start_value), method = 'SLSQP', bounds = allocs_bounds, constraints = alloc_constraints, options={'disp':True})
    # Store the results from the minimizer function
    allocs = min_result.x

    """ Compute the Portfolio Statistics """
    alloced = normed * allocs
    pos_value = alloced * start_value
    port_value = pos_value.sum(axis=1)
    daily_rets = compute_daily_returns(port_value)
    # Cumulative returns
    cr = (port_value[-1]/port_value[0]) - 1
    # Average Daily returns
    adr = daily_rets.mean()
    # Standard deviation of daily returns (Volatility)
    sddr = daily_rets.std()
    # Sharpe Ratio
    sharpe_ratio =  adr/sddr
    # Annualised Sharpe ratio with daily sampling frequency (252 trading days in a year)
    sr = np.sqrt(252) * sharpe_ratio

    # Get daily portfolio value
#    port_val = prices_SPY # add code here to compute daily portfolio values
    port_val = port_value/port_value[0]
    prices_SPY = prices_SPY/prices_SPY[0]

    print('port_val***************')
    print(port_val)
    print('prices_SPY***************')
    print(prices_SPY)
    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.DataFrame({'Portfolio':port_val, 'SPY':prices_SPY})
#       df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, title="Daily Portfolio value and SPY")
        pass

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
