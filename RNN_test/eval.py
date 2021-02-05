from LSTMModel import lstm
from dataset import getData
from parser_my import args
import torch


def eval():
    # model = torch.load(args.save_file)
    model = lstm(input_size=args.input_size, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)
    if args.useGPU:
        checkpoint = torch.load(args.save_file)
    else:
        checkpoint = torch.load(args.save_file,map_location=lambda storage, loc: storage)
    model.load_state_dict(checkpoint['state_dict'])
    preds = []
    labels = []
    close_max, close_min, train_loader, test_loader = getData(args.corpusFile, args.sequence_length, args.batch_size)
    # for idx, (x, label) in enumerate(test_loader):
    for idx, (x, label) in enumerate(train_loader):
        if args.useGPU:
            x = x.squeeze(1).cuda()  # batch_size,seq_len,input_size
        else:
            x = x.squeeze(1)
        pred = model(x)
        list = pred.data.squeeze(1).tolist()
        preds.extend(list[-1])
        labels.extend(label.tolist())
    # print(preds)
    count = 0
    acc = 0
    for i in range(len(preds)-1):
        # print('预测值是%.2f,真实值是%.2f'  % (
        # preds[i][0] * (close_max - close_min) + close_min, labels[i][0] * (close_max - close_min) + close_min))
        # print("%.2f" % preds[i][0],end=", ")
        if(preds[i][0]>0):
            print("预测会涨", end=", ")
        else:
            print("预测会跌", end=", ")
        if(labels[i]==1.0):
            print("实际涨了")
        else:
            print("实际跌了")
        if((preds[i][0]>=0 and labels[i]==1.0) or(preds[i][0]<=0 and labels[i]==-1.0)):
            acc+=1
        count+=1
    print(acc,count)
    print("实际预测准确率{0}%".format(acc*1.0/count*100))
        
        

eval()