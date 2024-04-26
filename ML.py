import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Input, Dropout
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from keras.models import Model


def split_dataset(x_data, split_ratio=0.6):
    Xtrain = x_data[:int(split_ratio * x_data.size)]
    Xtest = x_data[int(split_ratio * x_data.size):]

    return Xtrain, Xtest


def get_fitted_scalar(Xtrain):
    scaler = StandardScaler()
    scaler = scaler.fit(Xtrain)

    return scaler


def scale(Xtrain, scaler=None):
    if scaler is None:
        scaler = StandardScaler()
        scaler = scaler.fit(Xtrain)

    Xtrain = scaler.transform(Xtrain)

    return Xtrain


def to_sequences(x, y, seq_size=1):
    x_values = []
    y_values = []

    for i in range(x.size - seq_size):
        x_values.append(x[i:(i+seq_size)])
        y_values.append(y[i+seq_size])

    return np.array(x_values), np.array(y_values)


def get_model(trainX):
    model = Sequential()
    model.add(LSTM(128, activation='relu', input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
    model.add(LSTM(64, activation='relu', return_sequences=False))
    model.add((trainX.shape[1]))
    model.add(LSTM(64, activation='relu', return_sequences=True))
    model.add(LSTM(128, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(trainX.shape[2])))

    model.compile(optimizer='adam', loss='mse')
    model.summary()

    return model


def get_max_MAE(model, trainX):
    trainPredict = model.predict(trainX)
    trainMAE = np.mean(np.abs(trainPredict - trainX), axis=1)
    max_trainMAE = np.max(trainMAE) * 0.9

    return max_trainMAE


def model(data_buffer):
    seq_size = 30

    # print("Dataset received.")
    Xtrain, Xtest = split_dataset(data_buffer)
    # print("Dataset splitted.")
    scaler = get_fitted_scalar(Xtrain)
    Xtrain = scale(Xtrain, scaler)
    # print("Dataset scaled.")
    trainX, trainY = to_sequences(Xtrain, Xtrain, seq_size)
    # print("Splited to sequences.")
    model = get_model(trainX)
    # print("Model acquired.")

    model.fit(trainX, trainY, epochs=10, batch_size=32, validation_split=0.1, verbose=1)
    print("Fitting done.")

    return model



