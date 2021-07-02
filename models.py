import torch.nn as nn

class Shape(nn.Module):
    def __init__(self):
        super(Shape, self).__init__()
    
    def forward(self, x):
        print(x.shape)
        return x

class View(nn.Module):
    def __init__(self, shape):
        super(View, self).__init__()
        self.shape = shape
    
    def forward(self, x):
        return x.view(*self.shape)

class GatedActivation(nn.Module):
    def __init__(self):
        super(GatedActivation, self).__init__()
        self.tanh = nn.Tanh()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        t = self.tanh(x[:, :int(x.shape[1]/2)])
        s = self.sigmoid(x[:, int(x.shape[1]/2):])
        return t * s

# best acc: 98.67% train, 84.56% val
class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(72704, 1024),
            nn.Dropout(p=0.9),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.Dropout(p=0.9),
            nn.ReLU(),
            nn.Linear(512, 2),
            nn.Softmax(dim=1)
        )
    
    def forward(self, x):
        x = self.fc(x)
        return x

# best acc so far: 92.11% train, 82.78%, taking forever to train
class DeepMLP(nn.Module):
    def __init__(self):
        super(DeepMLP, self).__init__()
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(72704, 4096),
            nn.Dropout(p=0.9),
            nn.ReLU(),
            nn.Linear(4096, 2048),
            nn.Dropout(p=0.9),
            nn.ReLU(),
            nn.Linear(2048, 512),
            nn.Dropout(p=0.9),
            nn.ReLU(),
            nn.Linear(512, 2),
            nn.Softmax(dim=1)
        )
    
    def forward(self, x):
        x = self.fc(x)
        return x

# Hendler (2018)
# best acc: 96.94% train, 89.68% val
class ShallowCNN(nn.Module):
    def __init__(self):
        super(ShallowCNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 128, kernel_size=(71, 3), stride=1), # 71 for num of chars
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3)
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(14620, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            nn.Linear(1024, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            nn.Linear(1024, 2),
            nn.Softmax(dim=1)
        )
    
    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class GatedCNN(nn.Module):
    def __init__(self):
        super(GatedCNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 128, kernel_size=(71, 3), stride=1), # 71 for num of chars
            GatedActivation(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3)
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(14620, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            nn.Linear(1024, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            nn.Linear(1024, 2),
            nn.Softmax(dim=1)
        )
    
    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

# Zhang (2015)
# best acc: not run yet
class DeepCNN(nn.Module):
    def __init__(self):
        super(DeepCNN, self).__init__()
        self.conv = nn.Sequential(
            # conv1
            nn.Conv2d(1, 128, kernel_size=(71, 7), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 128, 339)),
            # conv2
            nn.Conv2d(1, 128, kernel_size=(128, 7), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 128, 111)),
            # conv3
            nn.Conv2d(1, 128, kernel_size=(128, 3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 128, 36)),
            # conv4
            nn.Conv2d(1, 128, kernel_size=(128, 3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 128, 11)),
            # conv5
            nn.Conv2d(1, 128, kernel_size=(128, 3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(384, 128),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            # output
            nn.Linear(128, 2),
            nn.Softmax(dim=1),
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class Conv2(nn.Module):
    def __init__(self):
        super(Conv2, self).__init__()
        self.conv = nn.Sequential(
            # conv1
            nn.Conv2d(1, 128, kernel_size=(71, 7), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 128, 339)),
            # conv2
            nn.Conv2d(1, 128, kernel_size=(128,3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1,3), stride=3),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(14336, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # fc2
            nn.Linear(1024, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # output
            nn.Linear(1024, 2),
            nn.Softmax(dim=1),
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class Conv2Gated(nn.Module):
    def __init__(self):
        super(Conv2Gated, self).__init__()
        self.conv = nn.Sequential(
            # conv1
            nn.Conv2d(1, 256, kernel_size=(71, 7), stride=1),
            GatedActivation(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 128, 339)),
            # conv2
            nn.Conv2d(1, 256, kernel_size=(128,3), stride=1),
            GatedActivation(),
            nn.MaxPool2d(kernel_size=(1,3), stride=3),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(14336, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # fc2
            nn.Linear(1024, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # output
            nn.Linear(1024, 2),
            nn.Softmax(dim=1),
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class LargeCNN2(nn.Module):
    def __init__(self):
        super(LargeCNN2, self).__init__()
        self.conv = nn.Sequential(
            # conv1
            nn.Conv2d(1, 1024, kernel_size=(71, 7), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 1024, 339)),
            # conv2
            nn.Conv2d(1, 1024, kernel_size=(1024,3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1,3), stride=3),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(114688, 2048),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # fc2
            nn.Linear(2048, 2048),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # output
            nn.Linear(2048, 2),
            nn.Softmax(dim=1),
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class Conv3(nn.Module):
    def __init__(self):
        super(Conv3, self).__init__()
        self.conv = nn.Sequential(
            # conv1
            nn.Conv2d(1, 128, kernel_size=(71, 7), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 128, 339)),
            # conv2
            nn.Conv2d(1, 128, kernel_size=(128, 3), stride=1),
            nn.ReLU(),
            View((-1, 1, 128, 337)),
            # conv3
            nn.Conv2d(1, 128, kernel_size=(128,3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1,3), stride=3),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(14208, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # fc2
            nn.Linear(1024, 1024),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # output
            nn.Linear(1024, 2),
            nn.Softmax(dim=1),
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class Conv4(nn.Module):
    def __init__(self):
        super(Conv4, self).__init__()
        self.conv = nn.Sequential(
            # conv1
            nn.Conv2d(1, 256, kernel_size=(71, 7), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 256, 339)),
            # conv2
            nn.Conv2d(1, 256, kernel_size=(256, 3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1,3), stride=3),
            View((-1, 1, 256, 112)),
            # conv3
            nn.Conv2d(1, 256, kernel_size=(256, 3), stride=1),
            nn.ReLU(),
            View((-1, 1, 256, 110)),
            # conv4
            nn.Conv2d(1, 256, kernel_size=(256,3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1,3), stride=3),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(9216, 1024),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            # fc2
            nn.Linear(1024, 1024),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            # output
            nn.Linear(1024, 2),
            nn.Softmax(dim=1),
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class Conv5(nn.Module):
    def __init__(self):
        super(Conv5, self).__init__()
        self.conv = nn.Sequential(
            # conv1
            nn.Conv2d(1, 256, kernel_size=(71, 7), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1, 3), stride=3),
            View((-1, 1, 256, 339)),
            # conv2
            nn.Conv2d(1, 256, kernel_size=(256, 3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1,3), stride=3),
            View((-1, 1, 256, 112)),
            # conv3
            nn.Conv2d(1, 256, kernel_size=(256, 3), stride=1),
            nn.ReLU(),
            View((-1, 1, 256, 110)),
            # conv4
            nn.Conv2d(1, 256, kernel_size=(256, 3), stride=1),
            nn.ReLU(),
            View((-1, 1, 256, 108)),
            # conv5
            nn.Conv2d(1, 256, kernel_size=(256,3), stride=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(1,3), stride=3),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(8960, 1024),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            # fc2
            nn.Linear(1024, 1024),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            # output
            nn.Linear(1024, 2),
            nn.Softmax(dim=1),
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

class SimpleLSTM(nn.Module):
    def __init__(self):
        super(SimpleLSTM, self).__init__()
        self.lstm = nn.LSTM(71, 256, batch_first=True)
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(262144, 256),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # fc2
            nn.Linear(256, 256),
            nn.Dropout(p=0.8),
            nn.ReLU(),
            # output
            nn.Linear(256, 2),
            nn.Softmax(dim=1),
        )
    
    # def forward(self, x, hn, cn):
    def forward(self, x):
        # x = self.lstm(x, (hn, cn))
        x, _ = self.lstm(x)
        x = self.fc(x)
        return x

class SmallLSTM(nn.Module):
    def __init__(self):
        super(SmallLSTM, self).__init__()
        self.lstm = nn.LSTM(71, 128, batch_first=True)
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(131072, 256),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            # fc2
            nn.Linear(256, 256),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            # output
            nn.Linear(256, 2),
            nn.Softmax(dim=1),
        )
    
    # def forward(self, x, hn, cn):
    def forward(self, x):
        # x = self.lstm(x, (hn, cn))
        x, _ = self.lstm(x)
        x = self.fc(x)
        return x

class LargeLSTM(nn.Module):
    def __init__(self):
        super(LargeLSTM, self).__init__()
        self.lstm = nn.LSTM(71, 512, batch_first=True)
        self.fc = nn.Sequential(
            nn.Flatten(),
            # fc1
            nn.Linear(524288, 256),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            # fc2
            nn.Linear(256, 256),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            # output
            nn.Linear(256, 2),
            nn.Softmax(dim=1),
        )
    
    # def forward(self, x, hn, cn):
    def forward(self, x):
        # x = self.lstm(x, (hn, cn))
        x, _ = self.lstm(x)
        x = self.fc(x)
        return x
