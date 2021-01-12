import tushare as ts
import datetime
#设置ts令牌
ts.set_token('9e60aeb25b1f43c7082ad0e9df9196e6b22c30cf0843398eb3ac091b')
pro = ts.pro_api()
#300274为股票代号，直接通过get_hist_data()获取的数据是逆序的，正序数据需要加上sort.index()
# 股票代码后面为SH或者SZ分别代表上海深圳
data = pro.daily(ts_code='601579.SH', start_date='20160101', end_date='20201229')
data = data.rename(columns={'vol': 'volume'})
data.set_index('trade_date', inplace=True)  # 设置索引覆盖原来的数据
data.index = list(map(lambda x: datetime.datetime.strptime(x, "%Y%m%d"), data.index))
data = data.sort_index(ascending=True)  # 将时间顺序升序，符合时间序列
print(data)
#选择需要标签存储股票数据
data.to_csv('./data/KuaiJSH_601579_2019to2020.csv', columns=['open','high','low','close','volume'])