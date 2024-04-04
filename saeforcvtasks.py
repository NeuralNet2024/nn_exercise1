# -*- coding: utf-8 -*-
"""SAEForCVtasks.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AsG8EFrehQAxNyJwSUjIJqQwtA-CA18l
"""

'''
Demonstrate the capabilites of a stacked autonencoder for computer vision tasks
https://blog.keras.io/building-autoencoders-in-keras.html
'''

# Import Packages
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import metrics
from keras.datasets import mnist
from tensorflow import keras as ks

#define the architecture as a function
def the_autoencoder():
# establish model's architecture using a Functional API
# here we explicitly declare what goes as input to each layer
  input_img = ks.Input(shape=(784,))
  encoded = ks.layers.Dense(128, activation='relu')(input_img)
  encoded = ks.layers.Dense(64, activation='relu')(encoded)
  encoded = ks.layers.Dense(32, activation='relu')(encoded)

  decoded = ks.layers.Dense(64, activation='relu')(encoded)
  decoded = ks.layers.Dense(128, activation='relu')(decoded)
  decoded = ks.layers.Dense(784, activation='sigmoid')(decoded)

  SAE = ks.Model(input_img, decoded)
  return SAE

#load the data
# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

#we are talking about RBG (gray here) images. Normalization is easy
x_train = x_train / 255
x_test = x_test/255

# do not forget the validate set
x_train, x_val, y_train, y_val =\
 train_test_split(x_train, y_train, test_size=0.1, random_state=1)

#build the SAE model
SAE = the_autoencoder()
SAE.summary()
SAE.compile(optimizer='adam', loss='binary_crossentropy')

#train the model
# use a per-pixel binary crossentropy loss, and the Adam optimizer
history = SAE.fit(x_train.reshape(-1,(28*28)),
        x_train.reshape(-1,(28*28)),
        epochs=10,
        batch_size=128,
        shuffle=True,
        validation_data=(x_val.reshape(-1,(28*28)), x_val.reshape(-1,(28*28))))

history.history.keys()

#plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history.history[list(history.history.keys())[0]])
plt.plot(history.history[list(history.history.keys())[1]])
plt.title('binary crossentropy error')
plt.ylabel(list(history.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

# Encode and decode some digits throught our SAE
# Note that we take them from the *test* set
restored_testing_dataset = SAE.predict(x_test.reshape(-1,(28*28)))

plt.figure(figsize=(20,5))
for i in range(10):
    index = y_test.tolist().index(i)
    plt.subplot(2, 10, i+1)
    plt.imshow(x_test[index].reshape((28,28)))
    plt.gray()
    plt.subplot(2, 10, i+11)
    plt.imshow(restored_testing_dataset[index].reshape((28,28)))
    plt.gray()

# now repeat above process by adding a noise factor to the images
noise_factor = 0.2
x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape) 
x_test_noisy = x_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape) 
x_val_noisy = x_val + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_val.shape)

x_train_noisy = np.clip(x_train_noisy, 0., 1.)
x_test_noisy = np.clip(x_test_noisy, 0., 1.)
x_val_noisy = np.clip(x_val_noisy, 0., 1.)

plt.figure(figsize=(20,5))
for i in range(10):
    index = y_test.tolist().index(i)
    plt.subplot(2, 10, i+1)
    plt.imshow(x_test[index].reshape((28,28)))
    plt.gray()
    plt.subplot(2, 10, i+11)
    plt.imshow(x_test_noisy[index].reshape((28,28)))
    plt.gray()

#train the model
denoise_SAE = the_autoencoder()
denoise_SAE.compile(optimizer='adam', loss='binary_crossentropy')

history = denoise_SAE.fit(x_train_noisy.reshape(-1,(28*28)),
        x_train.reshape(-1,(28*28)),
        epochs=30,
        batch_size=128,
        shuffle=True,
        validation_data=(x_val_noisy.reshape(-1,(28*28)), x_val.reshape(-1,(28*28))))

#plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history.history[list(history.history.keys())[0]])
plt.plot(history.history[list(history.history.keys())[1]])
plt.title('binary crossentropy error')
plt.ylabel(list(history.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

# Encode and decode some digits throught our SAE
# Note that we take them from the NOISY *test* set
denoised_testing_dataset = denoise_SAE.predict(x_test_noisy.reshape(-1,(28*28)))

plt.figure(figsize=(20,5))
for i in range(10):
    index = y_test.tolist().index(i)
    plt.subplot(2, 10, i+1)
    plt.imshow(x_test_noisy[index].reshape((28,28)))
    plt.gray()
    plt.subplot(2, 10, i+11)
    plt.imshow(denoised_testing_dataset[index].reshape((28,28)))
    plt.gray()

'''
Here we have some tranfer learning stuff!
https://keras.io/guides/transfer_learning/
'''

# now let's do some supervised learning!
#approach 1: a multilayer perceptron
#approach 2: Transfer learning using the encoded parts

#approach 1: define architecture
#for comparison purposes, same as the encoder
def FFNN(predifined_activation_map = 'softmax',\
              predifined_output_num = 10 ):
  input_img = ks.Input(shape=(784,))
  encoded = ks.layers.Dense(128, activation='relu')(input_img)
  encoded = ks.layers.Dense(64, activation='relu')(encoded)
  encoded = ks.layers.Dense(32, activation='relu')(encoded)

  classification_layer = ks.layers.Dense(predifined_output_num,\
                          activation=predifined_activation_map)(encoded)

  net = ks.Model(input_img, classification_layer)
  return net

#approach 1: compile and train the model
CustomModel = FFNN()

#plot the arhitecture
CustomModel.summary()

#define some training parameters
CustomModel.compile(optimizer='adam',\
                    loss=ks.losses.CategoricalCrossentropy(),\
                    metrics=[ks.metrics.AUC()])

#do the training
history = CustomModel.fit(x_train_noisy.reshape(-1,(28*28)),\
                          ks.utils.to_categorical(y_train),\
                          epochs=10,\
                          batch_size=128,\
                          shuffle=True,\
                          validation_data=\
                          (x_val.reshape(-1,(28*28)),\
                          ks.utils.to_categorical(y_val)))

#Appoach1: check the performance [TRAIN/ VALIDATION SETS ONLY!]
#1st plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history.history[list(history.history.keys())[0]])
plt.plot(history.history[list(history.history.keys())[2]])
plt.title('model root_mean_squared_error')
plt.ylabel(list(history.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

#2nd check networks' [predicted] outputs against actual outputs.
y_train_Predicted_SoftLabels = CustomModel.predict(x_train.reshape(-1,(28*28)))

#adjust networks outcomes remember that we get continuous values
#it is also likely to have more than one outputs, we need the argmax
if len(y_train_Predicted_SoftLabels.shape)>1:
  y_train_Predicted = np.argmax(y_train_Predicted_SoftLabels, axis=1)
else:
  y_train_Predicted = np.rint(y_train_Predicted_SoftLabels)


# plt.figure(figsize=(14,6))
# plt.plot( y_train, '+', label='original')
# plt.plot( y_train_Predicted, 'x', label='predicted')
# plt.title('Train set output values')
# plt.xlabel('input values')
# plt.ylabel('output values')
# plt.legend(loc='best')
# plt.show()  


#lastly the confusion matrix
confusion_matrix = metrics.confusion_matrix(y_train, y_train_Predicted)

cm_display =\
 metrics.ConfusionMatrixDisplay(confusion_matrix =\
 confusion_matrix)

plt.figure(figsize=(8,8))
cm_display.plot()
plt.show()

#approach 2: transfer learning

##load the pretrained model
#SAE = ks.models.load_model('fullpathname.hdf5')

#get the encoder part
encoder = ks.Model(SAE.input, SAE.layers[-4].output)

#check that you got the correct part (i.e. autoencoder only)
encoder.summary()

#make sure that you set all existing weights *untrainable*
encoder.trainable=False

encoder.summary()

#now create a new model on top, by adding classification layer
# transfer_based_FFNN =ks.Model(encoder,\
#                               ks.layers.Dense(10,\
#                               activation='softmax'))

inputs = ks.Input(shape=(784,))

# We make sure that the base_model is running in inference mode here,
# by passing `training=False`. 
tmp_var = encoder(inputs, training=False)

# A Dense classifier with n units (here n = 10)
classification_layer = ks.layers.Dense(10,\
                          activation='softmax')(tmp_var)

#finally build the transfer based model
transfer_based_FFNN =ks.Model(inputs, classification_layer)

transfer_based_FFNN.summary()

#define some training parameters
transfer_based_FFNN.compile(optimizer='adam',\
                            loss=ks.losses.CategoricalCrossentropy(),\
                            metrics=[ks.metrics.AUC()])


#now train a bit, but only the last added layer
#do the training
history = transfer_based_FFNN.fit(x_train_noisy.reshape(-1,(28*28)),\
                          ks.utils.to_categorical(y_train),\
                          epochs=10,\
                          batch_size=128,\
                          shuffle=True,\
                          validation_data=\
                          (x_val.reshape(-1,(28*28)),\
                          ks.utils.to_categorical(y_val)))

#Appoach 2 transfer lrng: check the performance [TRAIN/ VALIDATION SETS ONLY!]
#1st plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history.history[list(history.history.keys())[0]])
plt.plot(history.history[list(history.history.keys())[2]])
plt.title('model root_mean_squared_error')
plt.ylabel(list(history.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

#2nd check networks' [predicted] outputs against actual outputs.
y_train_Predicted_SoftLabels =\
 transfer_based_FFNN.predict(x_train.reshape(-1,(28*28)))

#adjust networks outcomes remember that we get continuous values
#it is also likely to have more than one outputs, we need the argmax
if len(y_train_Predicted_SoftLabels.shape)>1:
  y_train_Predicted = np.argmax(y_train_Predicted_SoftLabels, axis=1)
else:
  y_train_Predicted = np.rint(y_train_Predicted_SoftLabels)


# plt.figure(figsize=(14,6))
# plt.plot( y_train, '+', label='original')
# plt.plot( y_train_Predicted, 'x', label='predicted')
# plt.title('Train set output values')
# plt.xlabel('input values')
# plt.ylabel('output values')
# plt.legend(loc='best')
# plt.show()  


#lastly the confusion matrix
confusion_matrix = metrics.confusion_matrix(y_train, y_train_Predicted)

cm_display =\
 metrics.ConfusionMatrixDisplay(confusion_matrix =\
 confusion_matrix)

plt.figure(figsize=(8,8))
cm_display.plot()
plt.show()