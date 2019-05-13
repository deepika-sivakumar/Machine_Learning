Project 6 - Manual Strategy

Part 1 - Indicators

Filename: indicators.py
Purpose: Calculate the technical indicators using this file.
Steps:
	Import the file as, "import indicators as ind"
	To calculate Price/SMA ratio call the method as, "ind.calculate_price_SMA_ratio(price_symbol, symbols, lookback)"
	To calculate Bollinger band percentage call the method as , "ind.calculate_bbp(price_symbol, symbols, lookback)"
	To calculate Momentum call the method as, "ind.calculate_momentum(price, symbols, lookback)"

Market Simulator:
Filename: marketsimcode.py
Purpose: To compute Portfolio values and statistics.
Steps:
	Import the file as, "import marketsimcode as msim"
	To calculate the Portfolio or benchmark values, call the method as, "msim.compute_portvals(df_trades, start_val=start_value, commission=commission, impact=impact)"
	To calculate the Portfolio or benchmark statistics, call the method as, "msim.compute_stats(df_portvals)"
	
Part 2 - Theoretically Optimal Strategy

Filename: TheoreticallyOptimalStrategy.py
Purpose: Create trades based on theoretically optimal strategy.
Steps:
	Import the file as, "import TheoreticallyOptimalStrategy as TheoreticallyOptimalStrategy"
	Create an object of that class as, "tos = TheoreticallyOptimalStrategy()"
	To create trades for Portfolio as, "tos.testPolicy(symbol = "JPM", sd=start_date, ed=end_date, sv=start_value)"
	To create trades for Benchmark as, "tos.benchmark(sd=start_date, ed=end_date, sv=start_value)"

Part 3 - Manual Rule Based Trader

Filename: ManualStrategy.py
Purpose: Create trades based on the manual rule based strategy.
Steps:
	Import the file as, "import ManualStrategy as ManualStrategy"
	Create an object of that class as, "ms = ManualStrategy()"
	To create trades for Portfolio as, "ms.testPolicy(symbol = "JPM", sd=start_date, ed=end_date, sv=start_value)"
	To create trades for Benchmark as, "ms.benchmark(sd=start_date, ed=end_date, sv=start_value)"