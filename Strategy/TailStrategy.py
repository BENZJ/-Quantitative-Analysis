# TODO 
# 尾盘交易，如果前一天尾盘上涨(在两点至两点半呈现上涨，则买入)
# 如果尾盘呈现下跌趋势，则卖出，上涨则继续保留

import akshare as ak
import tushare as ts
if __name__ == "__main__":
    df = ts.get_realtime_quotes('000581') # 实时分笔
    print(df)