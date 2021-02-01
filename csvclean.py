import pandas as pd
import datetime
if __name__ == "__main__":
    data = pd.read_csv('./data/sh.csv')
    data = data.rename(columns={'vol': 'volume'})

    data = pd.DataFrame(data, columns=['ts_code','trade_date','open','high','low','close','volume'])
    # *修改日期
    data["trade_date"]=data["trade_date"].astype(str)
    data["trade_date"]=data["trade_date"].apply(lambda x : datetime.datetime.strptime(x,"%Y%m%d"))
    data = data.sort_values(by=["ts_code","trade_date"], ascending=[False,True])
    # data.reset_index(drop=True, inplace=True)
    data = data.drop(data.columns[[0]], axis=1)
    data = data.rename(columns={'trade_date': 'date'})
    data.to_csv('./data/sh_clean.csv', index=None)
