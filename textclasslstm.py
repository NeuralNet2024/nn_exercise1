# -*- coding: utf-8 -*-
"""textClassLSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TKspRmXDiYhXIV6KaPgIYKpV9Ue5CAfC
"""

import tensorflow as tf
from tensorflow.keras.datasets import reuters
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import metrics
import numpy as np
import gensim.downloader as api

import matplotlib.pyplot as plt

#Load the Reuters dataset
(X_train, y_train), (X_test, y_test) = reuters.load_data(num_words=10000, test_split=0.2)

#plot the lenght of the sequences, before converting them to same lenght 
lengths = [len(sequence) for sequence in X_train]
plt.hist(lengths, bins=100)
plt.title('Length Distribution')
plt.xlabel('Length')
plt.ylabel('Count')
plt.show()

# Convert the word indexes to sequences of equal length by padding
# or truncating them
maxlen = 500
X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)

# Convert the target labels to categorical vectors
num_classes = np.max(y_train) + 1
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

# Print the size of the training and testing sets
print('Number of training examples:', len(X_train))
print('Number of testing examples:', len(X_test))

# Create a histogram of the categories
plt.hist(y_train.argmax(axis=1), bins=num_classes)
plt.title('Distribution of Categories')
plt.xlabel('Category')
plt.ylabel('Number of Samples')
plt.show()

# Get the word index dictionary
word_index = reuters.get_word_index()

# print(category_names)
print(word_index)

# # Reverse the word index dictionary
# reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

# # Map the category label integers to their corresponding category names
# category_names = [reverse_word_index.get(i - 3, '?') for i in range(90)]

# Download pre-trained <something> embeddings
#takes time!!!
embedding_model = api.load('glove-wiki-gigaword-100')

# setup parameters for the embedding process
embedding_dim = 100
word_index = reuters.get_word_index()
vocab_size = len(word_index) + 1
embedding_matrix = np.zeros((vocab_size, embedding_dim))
for word, i in word_index.items():
    if i >= vocab_size:
        continue
    if word in embedding_model:
        embedding_matrix[i] = embedding_model[word]

# Define the LSTM model without pre-trained word2vec embeddings
model_no_w2v = Sequential()
model_no_w2v.add(Embedding(10000, embedding_dim, input_length=maxlen))
model_no_w2v.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model_no_w2v.add(Dense(num_classes, activation='softmax'))
model_no_w2v.compile(loss='categorical_crossentropy',\
                     optimizer='adam', metrics=[metrics.AUC()])

# Define the LSTM model with pre-trained word2vec embeddings
model_w2v = Sequential()
model_w2v.add(Embedding(vocab_size, embedding_dim, weights=[embedding_matrix],\
                        input_length=maxlen, trainable=False))
model_w2v.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model_w2v.add(Dense(num_classes, activation='softmax'))
model_w2v.compile(loss='categorical_crossentropy', optimizer='adam',\
                  metrics=[metrics.AUC()])

# Train the LSTM models
batch_size = 64
epochs = 4

#plot the arhitecture
model_no_w2v.summary()

#now train the model
history_no_w2v = model_no_w2v.fit(X_train, y_train, batch_size=batch_size,\
                                  epochs=epochs, validation_split=0.2)



#check the performance [TRAIN/ VALIDATION SETS ONLY!]
#1st plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history_no_w2v.history[list(history_no_w2v.history.keys())[0]])
plt.plot(history_no_w2v.history[list(history_no_w2v.history.keys())[2]])
plt.title('categorical crossentropy')
plt.ylabel(list(history_no_w2v.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

#plot the arhitecture
model_w2v.summary()

#now train the model
history_w2v = model_w2v.fit(X_train, y_train, batch_size=batch_size,\
                            epochs=epochs, validation_split=0.2)

#check the performance [TRAIN/ VALIDATION SETS ONLY!]
#1st plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history_w2v.history[list(history_w2v.history.keys())[0]])
plt.plot(history_w2v.history[list(history_w2v.history.keys())[2]])
plt.title('mcategorical crossentropy')
plt.ylabel(list(history_w2v.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()