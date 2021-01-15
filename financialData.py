import akshare as ak
import pandas as pd
from requests.api import get
import tushare as ts
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

ts.set_token('9e60aeb25b1f43c7082ad0e9df9196e6b22c30cf0843398eb3ac091b')
pro = ts.pro_api()

def get_interst(stock: str = "600004") -> float:
    """获取每股收益

    Args:
        stock (str, optional): 股票代码. Defaults to "600004".

    Returns:
        float: 最近一次财报返回的每股收益
    """  
    url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{stock}/ctrl/2020/displaytype/4.phtml"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")  
    year_context = soup.find(attrs={"id": "con02-1"}).find("table").find_all("a")
    year_list = [item.text for item in year_context]
    url = f"https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{stock}/ctrl/{year_list[0]}/displaytype/4.phtml"
    r = requests.get(url)
    temp_df = pd.read_html(r.text)[12].iloc[:, :-1]
    return(temp_df.iloc[2,1])

def get_name(stoke_code):
    '''通过股票代码导出公司名称'''
    dat = pro.query('stock_basic', fields='symbol,name')           
    company_name = list(dat.loc[dat['symbol'] == stoke_code].name)[0]
    return company_name

# df = pro.hs_const(hs_type='SZ').loc[:,"ts_code"]

df = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code')
df = df['ts_code']
# exit()
out_df = pd.DataFrame(columns=['股票代码','股票名称','当前价格', "万元收益"])
for i in tqdm(range( len(df))): 
    code = df[i].split('.')[0]
    price = float(ts.get_realtime_quotes(df[i].split('.')[0])['price'][0])
    if price==0:
        continue
    intrest = float(get_interst(code))
    new=pd.DataFrame({'股票代码':code,
                  '股票名称':get_name(code),
                  '当前价格':price,
                  '万元收益':intrest/price*10000},
                  index=[0]) 
    out_df = out_df.append(new, ignore_index=True)
out_df.to_csv("./data/最近一次财.csv")
