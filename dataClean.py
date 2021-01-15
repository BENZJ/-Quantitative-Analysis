import pandas as pd
import datetime
if __name__ == "__main__":
    data = pd.read_csv('./data/test.csv')
    # *修改vol列名为volume
    data = data.rename(columns={'vol': 'volume'})
    # *修改日期
    data["trade_date"]=data["trade_date"].astype(str)
    data["trade_date"]=data["trade_date"].apply(lambda x : datetime.datetime.strptime(x,"%Y%m%d"))
    data = data.sort_values(by=["ts_code","trade_date"], ascending=[False,True])
    data.reset_index(drop=True, inplace=True)
    data = data.drop(data.columns[[0]], axis=1)
    print(data)

    
