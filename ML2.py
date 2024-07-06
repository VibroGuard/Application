import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Input, Dropout
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from sklearn.preprocessing import StandardScaler


def split_dataset(x_data, split_ratio=0.6):
    """
    Split the dataset into training and testing sets based on a split ratio.

    Parameters
    ----------
    x_data : ndarray
        The input data to be split.
    split_ratio : float, optional
        The ratio of the dataset to be used as the training set. Default is 0.6.

    Returns
    -------
    Xtrain : ndarray
        The training set.
    Xtest : ndarray
        The testing set.
    """
    Xtrain = x_data[:int(split_ratio * x_data.size)]
    Xtest = x_data[int(split_ratio * x_data.size):]

    return Xtrain, Xtest


def get_fitted_scalar(Xtrain):
    """
    Fit a StandardScaler to the training data.

    Parameters
    ----------
    Xtrain : ndarray
        The training data to fit the scaler.

    Returns
    -------
    scaler : StandardScaler
        The fitted StandardScaler object.
    """
    scaler = StandardScaler()
    scaler = scaler.fit(Xtrain)

    return scaler


def scale(Xtrain, scaler=None):
    """
    Scale the training data using the provided scaler, or fit a new StandardScaler if none is provided.

    Parameters
    ----------
    Xtrain : ndarray
        The training data to scale.
    scaler : StandardScaler, optional
        The scaler to use for scaling. If None, a new StandardScaler is fitted and used. Default is None.

    Returns
    -------
    Xtrain : ndarray
        The scaled training data.
    """
    if scaler is None:
        scaler = StandardScaler()
        scaler = scaler.fit(Xtrain)

    Xtrain = scaler.transform(Xtrain)

    return Xtrain


def to_sequences(x, y, seq_size=1):
    """
    Convert the input data into sequences of the specified size.

    Parameters
    ----------
    x : ndarray
        The input data.
    y : ndarray
        The target data.
    seq_size : int, optional
        The size of each sequence. Default is 1.

    Returns
    -------
    x_values : ndarray
        The input data converted into sequences.
    y_values : ndarray
        The target data corresponding to the sequences.
    """
    x_values = []
    y_values = []

    for i in range(x.size - seq_size):
        x_values.append(x[i:(i + seq_size)])
        y_values.append(y[i + seq_size])

    return np.array(x_values), np.array(y_values)


def get_model(trainX):
    """
    Build and compile an LSTM model for sequence prediction.

    Parameters
    ----------
    trainX : ndarray
        The training data used to determine the input shape of the model.

    Returns
    -------
    model : Sequential
        The compiled LSTM model.
    """
    model = Sequential()
    model.add(LSTM(128, activation='relu', input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
    model.add(LSTM(64, activation='relu', return_sequences=False))
    model.add(RepeatVector(trainX.shape[1]))
    model.add(LSTM(64, activation='relu', return_sequences=True))
    model.add(LSTM(128, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(trainX.shape[2])))

    model.compile(optimizer='adam', loss='mse')
    model.summary()

    return model


def get_max_MAE(model, trainX):
    """
    Compute the maximum mean absolute error (MAE) of the model's predictions on the training data.

    Parameters
    ----------
    model : Sequential
        The trained LSTM model.
    trainX : ndarray
        The training data.

    Returns
    -------
    max_trainMAE : float
        The maximum mean absolute error scaled by 0.9.
    """
    trainPredict = model.predict(trainX)
    trainMAE = np.mean(np.abs(trainPredict - trainX), axis=1)
    max_trainMAE = np.max(trainMAE) * 0.9

    return max_trainMAE


def get_mae(model, xdata):
    """
    Compute the mean absolute error (MAE) of the model's predictions on the input data.

    Parameters
    ----------
    model : Sequential
        The trained LSTM model.
    xdata : ndarray
        The input data.

    Returns
    -------
    mae : ndarray
        The mean absolute error for each sequence in the input data.
    """
    predicted = model.predict(xdata)
    mae = np.mean(np.abs(predicted - xdata), axis=1)

    return mae


def model(data_buffer):
    """
    Train an LSTM model on the input data buffer.

    Parameters
    ----------
    data_buffer : ndarray
        The input data to train the model.

    Returns
    -------
    model : Sequential
        The trained LSTM model.
    max_MAE : float
        The maximum mean absolute error of the model's predictions on the training data.
    scaler : StandardScaler
        The fitted scaler used to scale the training data.

    Raises
    ------
    ValueError
        If the input data buffer is empty.
    """
    if len(data_buffer) == 0:
        raise ValueError("Empty dataset.")
    seq_size = 30

    Xtrain, Xtest = split_dataset(data_buffer)
    scaler = get_fitted_scalar(Xtrain)
    Xtrain = scale(Xtrain, scaler)
    trainX, trainY = to_sequences(Xtrain, Xtrain, seq_size)
    model = get_model(trainX)

    model.fit(trainX, trainY, epochs=10, batch_size=32, validation_split=0.1, verbose=1)

    max_MAE = get_max_MAE(model, trainX)

    return model, max_MAE, scaler


def predict(model, max_mae, scaler, xdata):
    """
    Predict anomalies in the input data using the trained LSTM model.

    Parameters
    ----------
    model : Sequential
        The trained LSTM model.
    max_mae : float
        The maximum mean absolute error threshold for anomaly detection.
    scaler : StandardScaler
        The fitted scaler used to scale the input data.
    xdata : ndarray
        The input data to be predicted.

    Returns
    -------
    anomaly_indices : ndarray
        The indices of the sequences in the input data that are considered anomalies.
    """
    seq_size = 30

    xdata = scale(xdata, scaler)
    xdata, ydata = to_sequences(xdata, xdata, seq_size)
    mae = get_mae(model, xdata)
    anomaly_indices = np.asarray(mae > max_mae).nonzero()[0]

    return anomaly_indices
