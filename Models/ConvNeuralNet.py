import pandas as pd
import numpy as np
import glob
from keras.preprocessing import image
import tensorflow as tf
import torch.nn as nn
import torch
import os

os.environ["CUDA_VISIBLE_DEVICES"]="-1"

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class makeNeuralNet(nn.Module):
    def     __init__(self):
        super(makeNeuralNet, self).__init__()
        kernelSize = (3,3)
        self.layer_1 = nn.Conv2d(in_channels = 3, out_channels = 32, kernel_size = kernelSize , stride=1, padding=1)
        self.pool_1 = nn.MaxPool2d(kernel_size = kernelSize, stride = 2, padding = 1)
        self.batch_1 = nn.BatchNorm2d(num_features=32)
        self.relu_1 = nn.ReLU()

        self.layer_2 = nn.Conv2d(in_channels = 32, out_channels = 64, kernel_size = kernelSize, stride=1, padding=1)
        self.pool_2 = nn.MaxPool2d(kernel_size = kernelSize, stride = 2, padding = 1)
        self.batch_2 = nn.BatchNorm2d(num_features=64)
        self.relu_2 = nn.ReLU()

        self.layer_3 = nn.Conv2d(in_channels = 64, out_channels = 128, kernel_size = kernelSize, stride=1, padding=1)
        self.pool_3 = nn.MaxPool2d(kernel_size = kernelSize, stride = 2, padding = 1)
        self.batch_3 = nn.BatchNorm2d(num_features=128)
        self.relu_3 = nn.ReLU()

        self.layer_4a = nn.Conv2d(in_channels = 128, out_channels = 256, kernel_size = kernelSize, stride=1, padding=1)
        self.layer_4b = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=kernelSize, stride=1, padding=1)
        self.pool_4 = nn.MaxPool2d(kernel_size = kernelSize, stride = 2, padding = 1)
        self.batch_4 = nn.BatchNorm2d(num_features=256)
        self.relu_4 = nn.ReLU()

        self.layer_5a = nn.Conv2d(in_channels = 256, out_channels = 512, kernel_size = kernelSize, stride=1, padding=1)
        self.layer_5b = nn.Conv2d(in_channels=512, out_channels=512, kernel_size=kernelSize, stride=1, padding=1)
        self.pool_5 = nn.MaxPool2d(kernel_size = 3, stride = 2, padding = 1)
        self.batch_5 = nn.BatchNorm2d(num_features=512)
        self.relu_5 = nn.ReLU()

        self.linear = nn.Linear(in_features = 512, out_features = 15)
        self.sigmoid = nn.LogSigmoid()

    def forward(self,picture):
        picture_layer_1 = self.pool_1(self.batch_1(self.relu_1(self.layer_1(picture))))
        picture_layer_2 = self.pool_2(self.batch_2(self.relu_2(self.layer_2(picture_layer_1))))
        picture_layer_3 = self.pool_3(self.batch_3(self.relu_3(self.layer_3(picture_layer_2))))
        picture_layer_4 = self.pool_4(self.batch_4(self.relu_4(self.layer_4b(self.layer_4a(picture_layer_3)))))
        picture_layer_5 = self.pool_5(self.batch_5(self.relu_5(self.layer_5b(self.layer_5a(picture_layer_4)))))
        linearFeatures = self.linear(picture_layer_5.flatten())

        return linearFeatures


dataset = pd.read_pickle(str('/home/tim/Desktop/OBP/project-klebsiella/Data/Pickle') + "/Processed_data_nn.pkl")

#def calculateOutputChannels(kernelWidth,Stride,Padding,channelsIn):
#    return (kernelWidth + 2 * padding)/Stride

def calculateFilterSize(Stride,Padding,channelsIn,channelsOut):
    return channelsIn + 2*Padding - channelsOut*Stride - Stride

net = makeNeuralNet()

#import torch.optim as optim

#criterion = nn.CrossEntropyLoss()
#optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
for epoch in range(20):  # loop over the dataset multiple times

    running_loss = 0.0

    listOfTensors = list(dataset['Image'])
    listOfLabels = list(dataset['Label'])

    for i,tensor in enumerate(listOfTensors):

        tensor = tensor.unsqueeze(0)
        output = net(tensor)
        label = listOfLabels[i]
        sigmoid = torch.nn.LogSigmoid()
        weight = sigmoid(output)

        crossEntropyLoss = torch.nn.CrossEntropyLoss()
        lossPerImage = crossEntropyLoss(weight,label)
        lossPerImage.backward()
        running_loss += lossPerImage.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

    print("FIRST EPOCH DONEZOS")

    '''
    for index,row in dataset.iterrows():
        # get the inputs
        inputs, labels = row
        inputs = inputs.unsqueeze(0)
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        #if i % 2000 == 1999:    # print every 2000 mini-batches
        #    print('[%d, %5d] loss: %.3f' %
        #          (epoch + 1, i + 1, running_loss / 2000))
        #    running_loss = 0.0
    '''
print('Finished Training')





