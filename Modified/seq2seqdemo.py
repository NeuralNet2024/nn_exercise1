# -*- coding: utf-8 -*-
"""seq2SeqDemo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TSXjLzgURCM7E1U8IGJxhXxeJur2mN_n
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, GRU, SimpleRNN
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# Generate sample data
np.random.seed(42)
seq_length = 10
input_dim = 1
output_dim = 1
num_samples = 1000

def generate_data(seq_length, num_samples):
    X = np.zeros((num_samples, seq_length, input_dim))
    y = np.zeros((num_samples, seq_length, output_dim))
    for i in range(num_samples):
        X[i, :, 0] = np.sin(np.linspace(0, 2*np.pi, seq_length))
        y[i, :, 0] = np.cos(np.linspace(0, 2*np.pi, seq_length))
    return X, y

X, y = generate_data(seq_length, num_samples)

# Split data into training and testing sets
train_ratio = 0.8
train_size = int(train_ratio * num_samples)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Plot sample data
plt.figure(figsize=(8, 4))
plt.plot(np.linspace(0, 2*np.pi, seq_length), X[0].flatten(), 'b-o', label='Input')
plt.plot(np.linspace(0, 2*np.pi, seq_length), y[0].flatten(), 'r-o', label='Output')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Sample Data')
plt.legend()
plt.show()

# Define model architecture and compile
model_lstm = Sequential()
model_lstm.add(LSTM(64, input_shape=(seq_length, input_dim),\
                    return_sequences=True))
model_lstm.add(Dense(output_dim))
model_lstm.compile(optimizer=Adam(), loss=MeanSquaredError())

model_rnn = Sequential()
model_rnn.add(SimpleRNN(64, input_shape=(seq_length, input_dim),\
                        return_sequences=True))
model_rnn.add(Dense(output_dim))
model_rnn.compile(optimizer=Adam(), loss=MeanSquaredError())

model_gru = Sequential()
model_gru.add(GRU(64, input_shape=(seq_length, input_dim),\
                  return_sequences=True))
model_gru.add(Dense(output_dim))
model_gru.compile(optimizer=Adam(), loss=MeanSquaredError())

# Train the models
epochs = 10
history_lstm = model_lstm.fit(X_train, y_train,\
                              epochs=epochs, validation_split=0.2)

#check the performance [TRAIN/ VALIDATION SETS ONLY!]
#1st plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history_lstm.history[list(history_lstm.history.keys())[0]])
plt.plot(history_lstm.history[list(history_lstm.history.keys())[1]])
plt.title('model root_mean_squared_error')
plt.ylabel(list(history_lstm.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

history_rnn = model_rnn.fit(X_train, y_train,\
                            epochs=epochs, validation_split=0.2)

#check the performance [TRAIN/ VALIDATION SETS ONLY!]
#1st plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history_rnn.history[list(history_rnn.history.keys())[0]])
plt.plot(history_rnn.history[list(history_rnn.history.keys())[1]])
plt.title('model root_mean_squared_error')
plt.ylabel(list(history_rnn.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

history_gru = model_gru.fit(X_train, y_train,\
                            epochs=epochs, validation_split=0.2)

#check the performance [TRAIN/ VALIDATION SETS ONLY!]
#1st plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history_gru.history[list(history_gru.history.keys())[0]])
plt.plot(history_gru.history[list(history_gru.history.keys())[1]])
plt.title('model root_mean_squared_error')
plt.ylabel(list(history_gru.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

# Evaluate the models
loss_lstm = model_lstm.evaluate(X_test, y_test)
loss_rnn = model_rnn.evaluate(X_test, y_test)
loss_gru = model_gru.evaluate(X_test, y_test)

print(f"LSTM loss: {loss_lstm}")
print(f"RNN loss: {loss_rnn}")
print(f"GRU loss: {loss_gru}")