import pandas as pd
import tushare as ts
import datetime
#设置ts令牌
# hs300_data=ts.get_hs300s()
# print(hs300_data)

ts.set_token('9e60aeb25b1f43c7082ad0e9df9196e6b22c30cf0843398eb3ac091b')
pro = ts.pro_api()

#获取沪股通成分
df = pro.hs_const(hs_type='SH') 
data = None
for index , row in df.iterrows():
    code = row['ts_code']
    if index == 0 :
        data = ts.pro_bar(ts_code=code, adj='qfq',start_date='20100101')
    else:
        # data.append(ts.pro_bar(ts_code=code, adj='qfq',start_date='20100101'), ignore_index=True)
        data = pd.concat([data, ts.pro_bar(ts_code=code, adj='qfq',start_date='20100101')], ignore_index=True)

data.to_csv('./data/sh.csv')




exit()
#300274为股票代号，直接通过get_hist_data()获取的数据是逆序的，正序数据需要加上sort.index()
# 股票代码后面为SH或者SZ分别代表上海深圳
# data = pro.daily(ts_code='600000.SH')
data = data.rename(columns={'vol': 'volume'})
data.set_index('trade_date', inplace=True)  # 设置索引覆盖原来的数据
data.index = list(map(lambda x: datetime.datetime.strptime(x, "%Y%m%d"), data.index))
data = data.sort_index(ascending=True)  # 将时间顺序升序，符合时间序列
print(data)
#选择需要标签存储股票数据
# data.to_csv('./data/KuaiJSH_601579_2019to2020.csv', columns=['open','high','low','close','volume'])