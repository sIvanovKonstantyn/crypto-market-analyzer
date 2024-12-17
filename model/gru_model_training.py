import numpy as np
from numpy import newaxis
import pandas as pd
from keras.layers import Dense, Activation, Dropout
from keras.layers import GRU, LSTM
from keras.models import Sequential
from keras import optimizers
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

Enrol_window = 100

sc = MinMaxScaler(feature_range=(0, 1))


def normalise_windows(window_data):
    normalized_data = []
    for window in window_data:
        normalized_window = [(float(p) / float(window[0])) for p in window]
        normalized_data.append(normalized_window)

    return normalized_data


def load_data(dataset_name, column, seq_len, normalise_window):
    data = dataset_name.loc[:, column]

    sequence_len = seq_len + 1
    result = []
    for index in range(len(data) - sequence_len):
        result.append(data[index: index + sequence_len])

    if normalise_window:
        result = normalise_windows(result)

    result = np.array(result)

    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    np.random.shuffle(train)
    x_train = train[:, :-1]
    y_train = train[:, -1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    return [x_train, y_train, x_test, y_test]


def predict_sequence_full(model, data, windows_size):
    current_frame = data[0]
    predicted = []
    for i in range(len(data)):
        predicted.append(model.predict(current_frame[newaxis, :, :])[0, 0])
        current_frame = current_frame[1:]
        current_frame = np.insert(current_frame, [windows_size - 1], predicted[-1], axis=0)

    return predicted


def predict_sequences_multiple(model, data, windows_size, prediction_len):
    prediction_seqs = []
    for i in range(int(len(data) / prediction_len)):
        current_frame = data[i * prediction_len]
        predicted = []
        for j in range(prediction_len):
            predicted.append(model.predict(current_frame[newaxis, :, :])[0, 0])
            current_frame = current_frame[1:]
            current_frame = np.insert(current_frame, [windows_size - 1], predicted[-1])

        prediction_seqs.append(predicted)

    return prediction_seqs


def plot_results(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    ax.plot(predicted_data, label='Prediction')
    plt.legend()
    plt.show()


def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')

    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
        plt.legend()
    plt.show()


dataset = pd.read_csv('./trust-wallet-token-year.csv')
dataset['Date'] = pd.to_datetime(dataset['Date'], unit='ms')
dataset = dataset.set_index(['Date'])
dataset = dataset.sort_values(by='Date')

print(dataset.tail())


feature_train, label_train, feature_test, label_test = load_data(dataset, 'Close',
                                                                 Enrol_window, False)

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(feature_train.shape[1], 1)))
model.add(Dropout(0, 2))
model.add(LSTM(100, return_sequences=False))
model.add(Dropout(0, 2))
model.add(Dense(1, activation="linear"))

model.compile(loss='mse', optimizer='adam')

print('model compiled')
print(model.summary())

model.fit(feature_train, label_train, batch_size=512, epochs=50, validation_data = (feature_test, label_test))

predicted_stock_price = model.predict(feature_test)
plot_results(predicted_stock_price, label_test)
# print(label_test)

predictions = predict_sequences_multiple(model, feature_test, Enrol_window, 50)
plot_results_multiple(predictions, label_test, 50)