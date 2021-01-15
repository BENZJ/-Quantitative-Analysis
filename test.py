from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import backtrader as bt
import pandas as pd
import Strategy as st



if __name__ == '__main__':
    # Create a cerebro entity
    fromdate=datetime.datetime(2000, 1, 1),
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(st.RnnStrategy)

    datapath = './data/KuaiJSH_601579_2019to2020.csv'

    dataframe = pd.read_csv(datapath, index_col=0, parse_dates=True)    
    dataframe['openinterest'] = 0   
    data = bt.feeds.PandasData(dataname=dataframe,                               
                        fromdate=datetime.datetime(2019, 1, 1),                               
                        todate=datetime.datetime(2020, 1, 1)                               
    )    
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(10000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)

    # Set the commission
    cerebro.broker.setcommission(0.001)

    # Print out the starting conditions
    startValue = cerebro.broker.getvalue()
    print('初始资金: %.2f' % startValue)

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('结束资金: %.2f ,总共盈亏 %.2f' % (cerebro.broker.getvalue(), cerebro.broker.getvalue()-startValue))

    # Plot the result
    # cerebro.plot()