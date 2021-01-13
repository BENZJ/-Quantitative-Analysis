import backtrader as bt
import backtrader.indicators as btind

class RnnStrategy(bt.Strategy):
        
    params = dict(period=20)

    def __init__(self):
        """初始化一些参数
        self.datas 用来存储feed进来的数据
        SimpleMovingAverage 方法应该会生成一条叫做sma的lines
        """
        # sma = btind.SimpleMovingAverage(self.data, period=self.params.period)
        self.movav = btind.SimpleMovingAverage(self.data, period=self.p.period)
        pass

    def log(self, txt:str, dt=None):
        """统一日志输出
        
        Args:
            txt (str): 日志文本
            dt ([type], optional): 日期. Defaults to None.
        """        
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        """在这里写每日策略，回测的时候每一条数据都会进入一遍
        # TODO 通过RNN返回结果预测明日股票涨跌，如果涨则买入
        # ? 1.基本策略：1.持有不超过3天 2.如果涨幅大于10%则卖出 3.如果跌幅超过10%则卖出

        """        
        pass
    # def prenext(self):
    #     print('prenext:: current period:', len(self))

    # def nextstart(self):
    #     print('nextstart:: current period:', len(self))
    #     # emulate default behavior ... call next
    #     self.next()

    # def next(self):
    #     print('next:: current period:', len(self))