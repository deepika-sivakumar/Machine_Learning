"""
Market Simulator
""" 
 
import pandas as pd 
import numpy as np 
import datetime as dt 
import os 
from util import get_data, plot_data 

def author():
    return 'dsivakumar6'

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005): 
    # this is the function the autograder will call to test your code 
    # NOTE: orders_file may be a string, or it may be a file object. Your 
    # code should work correctly with either input 

    # My code
    # Get the orders data
    df_orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])

    # Sort the orders by date
    df_orders = df_orders.sort_index()

    # Get the start date & end date
    start_date = df_orders.index.min()
    end_date = df_orders.index.max() 
    dates = pd.date_range(start_date, end_date)

    # Get the symbols traded
    df_symbols_all = df_orders['Symbol']
    # Get the unique symbols alone
    df_symbols_temp = df_symbols_all.drop_duplicates()
    # Convert it into a list
    syms = df_symbols_temp.values.tolist()

    # Get all the prices of the symbols
    df_prices_all = get_data(syms, dates)  # automatically adds SPY
    df_prices = df_prices_all[syms]  # only portfolio symbols 

    # Add "Cash" column to the df_prices, initializing all values to 1.0
    df_prices['Cash'] = 1.0
    print('*********************df_prices*************************')
    print(df_prices)

    #Step2 - Trades Dataframe
    # Make a copy of the df_prices
    df_trades = df_prices.copy()
    df_trades[:] = 0

    # Iterate through the orders dataframe and calculate the shares & cash values for df_trades
    for index, row in df_orders.iterrows():
        orders_symbol = row['Symbol'] # Get the symbol
        order_type = row['Order'] # Get the Order type (BUY/SELL)
        symbol_price = df_prices.at[index, orders_symbol] # Get the Adjusted close price of that symbol on that date from df_prices
        # Set the No. of Shares traded from the df_orders to df_trades dataframe
        if(order_type == 'BUY'):
            # If its a "BUY" order we have gained the shares, so add
            df_trades.at[index, orders_symbol] = df_trades.at[index, orders_symbol] + row['Shares']
            #Calculate Cash = Sum_of_each_symbol_traded(No_Shares * Share_Price)
            trade_cost = row['Shares'] * symbol_price
            trade_impact = row['Shares'] * symbol_price * impact
            #If its a "BUY" order subtract (since we have spent that cash to buy)
            df_trades.at[index, 'Cash'] = df_trades.at[index, 'Cash'] - (trade_cost) - (trade_impact + commission)
        else:
            # If its a "SELL" order we have sold the shares, so subtract
            df_trades.at[index, orders_symbol] = df_trades.at[index, orders_symbol] - row['Shares']
            #Calculate Cash = Sum_of_each_symbol_traded(No_Shares * Share_Price)
            trade_cost = row['Shares'] * symbol_price
            trade_impact = row['Shares'] * symbol_price * impact
            #If its a "SELL" order add (since we have received that cash by selling)
            df_trades.at[index, 'Cash'] = df_trades.at[index, 'Cash'] + (trade_cost) - (trade_impact + commission)
#    print('***********************df_trades*************************')
#    print(df_trades)
    #Step 3 - Holdings Dataframe - How much asset value are you holding each day?
    df_holdings = df_trades.copy()
    # Add the Start Value to the First day cash
    df_holdings.at[start_date,'Cash'] = start_val + df_holdings.at[start_date,'Cash']
    # Add each row to the previous row values
    df_holdings = df_holdings.cumsum()
#    print('***********************df_holdings***********************')
#    print(df_holdings)
    #Step 4 df_values = df_prices * df_holdings
    df_values = df_prices * df_holdings
#    print('**********************df_values*************************')
#    print(df_values)
    #Step 5 Daily Portfolio Values
    df_portvals = df_values.sum(axis=1)
#    print('*********************df_portvals************************')
#    print(df_portvals)
    return df_portvals

#Function to compute SPX port_vals
def compute_portvals_SPX(prices_SPX, start_value):
    normed = prices_SPX/prices_SPX.values[0]
    alloced = normed
    pos_value = alloced * start_value
    port_vals_SPX = pos_value.sum(axis=1)
    return port_vals_SPX

#Function to compute portfolio statistics
def compute_stats(port_vals):
#    daily_rets = compute_daily_returns(port_vals)
    daily_rets = (port_vals/port_vals.shift(1)) - 1
    cr = (port_vals[-1]/port_vals[0]) - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sharpe_ratio=  adr/sddr
    sr = np.sqrt(252)*sharpe_ratio
    return cr, adr, sddr, sr

#Function to Compute the daily returns
def compute_daily_returns(port_vals):
    daily_returns = port_vals.copy()
    daily_returns[1:] =(port_vals[1:]/port_vals[:-1]) - 1
    daily_returns = daily_returns[1:]
    return daily_returns


def test_code(): 
    # this is a helper function you can use to test your code 
    # note that during autograding his function will not be called. 
    # Define input parameters 

    of = "./orders/orders2.csv" 
#    of = "./orders/orders-short.csv"
#    of = "./orders/orders.csv"
    sv = 1000000 

    # Process orders 
    portvals = compute_portvals(orders_file = of, start_val = sv) 
    if isinstance(portvals, pd.DataFrame): 
        portvals = portvals[portvals.columns[0]] # just get the first column 
    else: 
        "warning, code did not return a DataFrame" 

    # Compute Portfolio Statistics
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_stats(portvals)

    # Compute the SPY Statistics
    # Get the orders data to get the date range
    df_orders = pd.read_csv(of, index_col='Date', parse_dates=True, na_values=['nan'])
    start_date = df_orders.index.min()
    end_date = df_orders.index.max()
    dates = pd.date_range(start_date, end_date)
    # Get the prices of SPX
    prices_SPX = get_data(['$SPX'], dates)
    # Compute portvals of SPX
    portvals_SPX = compute_portvals_SPX(prices_SPX, sv)
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = compute_stats(portvals_SPX) 

    # Compare portfolio against $SPX 
    print "Date Range: {} to {}".format(start_date, end_date) 
    print 
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio) 
    print "Sharpe Ratio of SPX : {}".format(sharpe_ratio_SPX) 
    print 
    print "Cumulative Return of Fund: {}".format(cum_ret) 
    print "Cumulative Return of SPX : {}".format(cum_ret_SPX) 
    print 
    print "Standard Deviation of Fund: {}".format(std_daily_ret) 
    print "Standard Deviation of SPX : {}".format(std_daily_ret_SPX) 
    print 
    print "Average Daily Return of Fund: {}".format(avg_daily_ret) 
    print "Average Daily Return of SPX : {}".format(avg_daily_ret_SPX) 
    print 
    print "Final Portfolio Value: {}".format(portvals[-1]) 

if __name__ == "__main__": 
    test_code() 
