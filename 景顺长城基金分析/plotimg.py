import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib
import brewer2mpl
bmap = brewer2mpl.get_map('set3', 'qualitative', 12)
colors = bmap.mpl_colors
plt.style.use('ggplot')
     
# print(plt.style.available) 

stocklist = pd.read_csv('top_detail.csv')
stocklist['top_detail_report_date'] = pd.to_datetime(stocklist['top_detail_report_date']).dt.date
s_date_start = datetime.datetime.strptime('2020-03-24', '%Y-%m-%d').date()
s_date_stop = datetime.datetime.strptime('2020-08-24', '%Y-%m-%d').date()
stocklist = stocklist[stocklist['top_detail_report_date']>=s_date_start ]
stocklist = stocklist[stocklist['top_detail_report_date']<=s_date_stop ]
stocklist = stocklist[stocklist['top_detail_type']=='股票' ]

codeset = set(stocklist['top_detail_position_symbol'])
plt.title('景顺长城新兴成长混合股票持有情况')
for code in codeset:
    x = []
    y = []
    l_label = None
    for index, row in stocklist[stocklist['top_detail_position_symbol']==code].iterrows():
        # print(row)
        x.append(row['top_detail_amount'])
        y.append(row['top_detail_report_date'])
        l_label = row['top_detail_position_symbol']+"_"+row['top_detail_name']  
    l1=plt.plot(y,x,'o-',label=l_label)
plt.legend()
# plt.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=colors)
plt.show()

    