import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib
import tushare as ts
plt.style.use('ggplot')

stocklist = pd.read_csv('position_detail.csv')
stocklist['position_detail_report_date'] = pd.to_datetime(stocklist['position_detail_report_date']).dt.date

s_date_start = datetime.datetime.strptime('2020-07-24', '%Y-%m-%d').date()
s_date_stop = datetime.datetime.strptime('2020-08-24', '%Y-%m-%d').date()
stocklist = stocklist[stocklist['position_detail_report_date']>=s_date_start ]
stocklist = stocklist[stocklist['position_detail_report_date']<=s_date_stop ]
stocklist = stocklist[stocklist['position_detail_type']=='股票' ]
codeset = set(stocklist['position_detail_position_symbol'])

amount = []
label = []
for index, row in stocklist.iterrows():
    amount.append(row['position_detail_value'])
    label.append(row['position_detail_name'])
    pass
plt.pie(amount, labels=label)
plt.show()
pro = ts.pro_api()
for code in codeset:
    df = ts.pro_bar(ts_code=code, start_date='20200401')
    name = stocklist[stocklist['position_detail_position_symbol']==code ]['position_detail_name']
    # print(name.iat[0])
    updown = (-df.loc[df.index[-1]]['open']+df.loc[0]['open'])/df.loc[df.index[-1]]['open']*100
    print('股票:{0} 四月份价格为{1}: , 如今价格为:{2} , 涨幅{3:.2f}%'.format(name.iat[0],df.loc[df.index[-1]]['open'],df.loc[0]['open'],updown))
    # print(df)
