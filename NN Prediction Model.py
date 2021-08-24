import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard

import time
NAME = 'DigiRecognizer-CNN-{}'.format(int(time.time()))
tensorboard = TensorBoard(log_dir='logs\{}'.format(NAME))

def readData(fp):                   # 这里主要是把读取的POI和OD数据转换成12769(113*113)*N的形式，N是维度，对于POI是32维(一个点16，一OD对32)，对于OD是一维，即OD流量
    od = pd.read_excel(fp[0])
    poi = pd.read_excel(fp[1])
    zeroAppend = pd.DataFrame([np.array(['{}'.format(i).zfill(3)+'-'+'{}'.format(i).zfill(3)] + [0 for j in range(18)]) for i in range(1,114)], columns=od.columns)
    od = pd.concat([od, zeroAppend],axis=0).sort_values(by='od').reset_index(drop=True)
    od[od.columns[1:]] = od[od.columns[1:]].astype(int)
    od = od.values
    odTime = np.array([od[:,i] for i in range(1,19)]).T
    poi = poi.values[:,2:]
    poiData = np.array([poi[i].tolist()+poi[j].tolist() for i in range(0,113) for j in range(0,113)])
    return odTime, poiData


def nnModel():                      # 模型结构
    model = Sequential()
    model.add(Dense(200))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    model.add(Dense(200))
    model.add(Activation('relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1))
    model.add(Activation('relu'))
    adam = Adam(lr=1e-3)
    model.compile(optimizer=adam, loss='mse',metrics=['mae'])
    return model


def modelTrain(X_train, y_train, model, savefp):        # 训练过程
    history = model.fit(X_train, y_train, epochs=300, validation_split=0.1, callbacks=[tensorboard])
    plt.plot(history.epoch, history.history['loss'], label='train_loss')
    plt.plot(history.epoch, history.history['val_loss'], label='test_loss')
    plt.ylim(0, 1500)
    plt.legend()
    plt.show()
    model.save(savefp)


def dataDivide(odTime, poiData):
    pass

def shuffle_np(X, Y):
    Y = Y.reshape(len(Y), 1)
    data = np.concatenate([X, Y], axis=-1)
    np.random.seed(48)
    np.random.shuffle(data)
    X = data[:, :-1]
    Y = data[:, -1]
    return X, Y

def main(i):                                            # 主函数，i是时间段在表中是第几列
    fp = [r'OD.xlsx', r'POI-normalized data.xlsx']
    odTime, poiData = readData(fp)
    X = poiData
    y = odTime[:,i]
    X, y = shuffle_np(X, y)
    model = nnModel()
    modelTrain(X, y, model, 'save-17.h5')

if __name__ == '__main__':
    main(11)
