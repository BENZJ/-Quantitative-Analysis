from torch.autograd import Variable
import torch.nn as nn
import torch
from LSTMModel import lstm
from dataset import getData
from parser_my import args

def train():

    model = lstm(input_size=args.input_size, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1, dropout=args.dropout, batch_first=args.batch_first )
    model.to(args.device)

    # 是否需要继续训练
    if args.useGPU:
        checkpoint = torch.load(args.save_file)
    else:
        checkpoint = torch.load(args.save_file,map_location=lambda storage, loc: storage)
    model.load_state_dict(checkpoint['state_dict'])

    criterion = nn.MSELoss()  # 定义损失函数
    # optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)  # Adam梯度下降  学习率=0.001
    optimizer = torch.optim.RMSprop(model.parameters(), lr=args.lr)

    close_max, close_min, train_loader, test_loader = getData(args.corpusFile,args.sequence_length,args.batch_size )
    for i in range(args.epochs):
        total_loss = 0
        for idx, (data, label) in enumerate(train_loader):
            if args.useGPU:
                data1 = data.squeeze(1).cuda()
                pred = model(Variable(data1).cuda())
                # print(pred.shape)
                pred = pred[1,:,:]
                label = label.unsqueeze(1).cuda()
                # print(label.shape)
            else:
                data1 = data.squeeze(1)
                pred = model(Variable(data1))
                pred = pred[1, :, :]
                label = label.unsqueeze(1)
            loss = criterion(pred, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        if i % args.saveepochs == 0:
            # torch.save(model, args.save_file)
            torch.save({'state_dict': model.state_dict()}, args.save_file)
            print('第%d epoch，保存模型' % i)
            print(total_loss)
    # torch.save(model, args.save_file)
    torch.save({'state_dict': model.state_dict()}, args.save_file)

train()