from pandas import read_csv
import numpy as np
from torch.utils.data import DataLoader,Dataset
import torch
from torchvision import transforms

#
def getData(corpusFile,sequence_length,batchSize):
    # 数据预处理 ，去除id、股票代码、前一天的收盘价、交易日期等对训练无用的无效数据
    stock_data = read_csv(corpusFile)
    stock_data.drop('date', axis=1, inplace=True)

    close_max = stock_data['close'].max() #收盘价的最大值
    close_min = stock_data['close'].min() #收盘价的最小值
    df = stock_data.apply(lambda x: (x - min(x)) / (max(x) - min(x)))  # min-max标准化

    # 构造X和Y
    #根据前n天的数据，预测未来一天的收盘价(close)， 例如：根据1月1日、1月2日、1月3日、1月4日、1月5日的数据（每一天的数据包含8个特征），预测1月6日的收盘价。
    sequence = sequence_length
    X = []
    Y = []
    for i in range(df.shape[0] - sequence):
        X.append(np.array(df.iloc[i:(i + sequence), ].values, dtype=np.float32))
        if (df.iloc[(i + sequence), 3]>df.iloc[(i + sequence-1), 3]):
            updown = 1.0
        else:
            updown = -1.0
        # Y.append(np.array([df.iloc[(i + sequence), 3],updown], dtype=np.float32))
        Y.append(np.array(updown, dtype=np.float32))
        # Y.append(np.array(df.iloc[(i + sequence), 3], dtype=np.float32))

    # 构建batch
    total_len = len(Y)
    # print(total_len)

    trainx, trainy = X[:int(0.90 * total_len)], Y[:int(0.90 * total_len)]
    testx, testy = X[int(0.90 * total_len):], Y[int(0.90 * total_len):]
    train_loader = DataLoader(dataset=Mydataset(trainx, trainy, transform=transforms.ToTensor()), batch_size=batchSize,
                              shuffle=True)
    test_loader = DataLoader(dataset=Mydataset(testx, testy), batch_size=batchSize, shuffle=False)
    return close_max,close_min,train_loader,test_loader



class Mydataset(Dataset):
    def __init__(self, xx, yy, transform=None):
        self.x = xx
        self.y = yy
        self.tranform = transform

    def __getitem__(self, index):
        x1 = self.x[index]
        y1 = self.y[index]
        if self.tranform != None:
            return self.tranform(x1), y1
        return x1, y1

    def __len__(self):
        return len(self.x)

if __name__ == "__main__":
    corpusFile = "../data/KuaiJSH_601579_2019to2020.csv"
    close_max,close_min,train_loader,test_loader = getData(corpusFile, 1,64)
    for idx, (data, label) in enumerate(test_loader):
        print(idx)
        print(label)
        break
    pass
