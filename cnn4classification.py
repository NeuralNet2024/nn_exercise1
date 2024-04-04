# -*- coding: utf-8 -*-
"""CNN4Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1goosV02zm_ftq3cXNaIlOgeivgCWabus
"""

#import core module
from tensorflow import keras

#other usefull materials
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
import matplotlib.pyplot as plt
import random
import numpy as np

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

#normalize data in range [0,1]
# a grayscale image has values in [0,255]
x_train = x_train/255
x_test = x_test/255

# plot 9 images as gray scale
plt.subplot(331)
plt.imshow(x_train[0], cmap=plt.get_cmap('gray'))
plt.subplot(332)
plt.imshow(x_train[1], cmap=plt.get_cmap('gray'))
plt.subplot(333)
plt.imshow(x_train[2], cmap=plt.get_cmap('gray'))
plt.subplot(334)
plt.imshow(x_train[3], cmap=plt.get_cmap('gray'))
plt.subplot(335)
plt.imshow(x_train[4], cmap=plt.get_cmap('gray'))
plt.subplot(336)
plt.imshow(x_train[5], cmap=plt.get_cmap('gray'))
plt.subplot(337)
plt.imshow(x_train[6], cmap=plt.get_cmap('gray'))
plt.subplot(338)
plt.imshow(x_train[7], cmap=plt.get_cmap('gray'))
plt.subplot(339)
plt.imshow(x_train[8], cmap=plt.get_cmap('gray'))
# show the plot
plt.show()
plt.pause(4)

#do some informative plotting
print('Input data (train) shape is:', x_train.shape)
print('Input data (test) shape is:', x_test.shape)

print('Output data (train) shape is:', y_train.shape)
print('Output data (test) shape is:', y_test.shape)

print('Train set has the following classes:', np.unique(y_train))
print('Test set has the following classes:', np.unique(y_test))

# do a one-hot-encoding for the outputs
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

#check the outputs' range (just to be sure)
print(np.max(x_train))
print(np.min(x_train))

# create a CNN structure

my_cnn = Sequential()
my_cnn.add(keras.Input(shape=(28,28,1)))
my_cnn.add(Conv2D(6, kernel_size=(3,3), activation='relu'))
my_cnn.add(MaxPooling2D(pool_size=(2,2)))
my_cnn.add(Conv2D(12, kernel_size=(3,3), activation='relu'))
my_cnn.add(MaxPooling2D(pool_size=(2,2)))
my_cnn.add(Flatten())
my_cnn.add(Dense(128, activation = 'sigmoid'))
my_cnn.add(Dense(10, activation = 'softmax'))

#compile the model
my_cnn.compile(loss=keras.losses.categorical_crossentropy,\
               optimizer='Adam',\
               metrics=['accuracy'])

#and print its summary
my_cnn.summary()

# now train the CNN network
history = my_cnn.fit(x_train, y_train, batch_size=125, validation_split=0.1, epochs =20)

#part 3c: check the performance [TRAIN/ VALIDATION SETS ONLY!]
#1st plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history.history[list(history.history.keys())[0]])
plt.plot(history.history[list(history.history.keys())[2]])
plt.title('Cross entropy')
plt.ylabel(list(history.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

#use the trained model to calculate the outputs for both train and test sets
y_train_predicted = my_cnn.predict(x_train)
y_test_predicted = my_cnn.predict(x_test)

#demonstrtrating what the CNN output will be.
print('this is a typical CNN output:', y_train_predicted[0,:]

#convert CNN outputs to categorical, i.e. 0, 1, 2, ..., numofClasses
y_train_predicted = np.argmax(y_train_predicted, axis=1)
y_test_predicted = np.argmax(y_test_predicted, axis=1)

#do some plots to illustrate the results
class_to_demonstrate = 0

while (sum(y_test_predicted == class_to_demonstrate) > 4):
    tmp_idxs_to_use = np.where(y_test_predicted == class_to_demonstrate)

    # create new plot window
    plt.figure()

    # plot 4 images as gray scale
    plt.subplot(221)
    plt.imshow(x_test[tmp_idxs_to_use[0][0], :, :], cmap=plt.get_cmap('gray'))
    plt.subplot(222)
    plt.imshow(x_test[tmp_idxs_to_use[0][1], :, :], cmap=plt.get_cmap('gray'))
    plt.subplot(223)
    plt.imshow(x_test[tmp_idxs_to_use[0][2], :, :], cmap=plt.get_cmap('gray'))
    plt.subplot(224)
    plt.imshow(x_test[tmp_idxs_to_use[0][3], :, :], cmap=plt.get_cmap('gray'))
    tmp_title = 'Digits considered as' + str(class_to_demonstrate)
    plt.suptitle(tmp_title)

    # show the plot
    plt.show()
    plt.pause(2)

    # update the class to demonstrate index
    class_to_demonstrate = class_to_demonstrate + 1

#saving the *trained* model as an h5 file
my_cnn.save('aaa.h5')