# -*- coding: utf-8 -*-
"""predictNextCharLSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eIcRxBgcUxUUx_gu-dTw3OxCbC0kGYAb
"""

# Import necessary libraries
import tensorflow as tf
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt

# #Step 0: Load your file
# from google.colab import files
# uploaded = files.upload()
from google.colab import drive
drive.mount('/content/gdrive')

# Step 1: Load the Moby Dick book
with open("/content/gdrive/MyDrive/Datasets/BooksInUTF/Mobi Dick.txt", 'r', encoding='utf-8') as file:
    text = file.read()

from google.colab import drive
drive.mount('/content/drive')

# Step 2: Pre-process the text
text = text.replace('\n', '').replace('\r', '').replace('\ufeff', '').replace('“','').replace('”','')  #new line, carriage return, unicode character --> replace by space
text = text.lower()  #convert all characters to lowercase

# Step 3: Convert the text into a sequence of characters
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(text)
text_sequences = tokenizer.texts_to_sequences([text])[0]

# Step 4: Define the input and target sequences
max_len = 100
step = 5
input_sequences = []
target_sequences = []
for i in range(max_len, len(text_sequences), step):
  input_seq = text_sequences[i-max_len:i]
  target_seq = text_sequences[i]
  input_sequences.append(input_seq)
  target_sequences.append(target_seq)

# Step 5: Convert the input and target sequences into numpy arrays
input_sequences = np.array(input_sequences)
target_sequences = np.array(target_sequences)

# Step 6: Convert the target variable into one-hot encoded format
num_classes = len(tokenizer.word_index)+1
target_sequences = to_categorical(target_sequences, num_classes=num_classes)

# Step 7: Define the LSTM model
model = Sequential()
model.add(Embedding(input_dim=num_classes, output_dim=128, input_length=max_len))
model.add(LSTM(units=128))
model.add(Dense(units=num_classes, activation='softmax'))

# Step 8: Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 9: Train the model
history = model.fit(input_sequences, target_sequences,\
                    batch_size=128, epochs=22,\
                    validation_split=0.2)

#check the performance [TRAIN/ VALIDATION SETS ONLY!]
#1st plot the history performance scores
plt.figure(figsize=(14,6))
plt.plot(history.history[list(history.history.keys())[0]])
plt.plot(history.history[list(history.history.keys())[2]])
plt.title('model root_mean_squared_error')
plt.ylabel(list(history.history.keys())[0])
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()

# Step 10: Function to generate text
def generate_text(seed_text, next_chars, model, max_sequence_len):
  for _ in range(next_chars):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')
    predicted = model.predict_classes(token_list, verbose=0)
    output_char = tokenizer.index_word[predicted[0]]
    seed_text += output_char
  return seed_text

# Step 11: Generate text
# seed_text = "call me ishmael. some years ago—"
seed_text = "Once upon a time"
next_chars = 200
max_sequence_len = 100
generated_text = ""
for i in range(next_chars):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')
    predicted = model.predict(token_list, verbose=0)
    output_char = tokenizer.index_word[np.argmax(predicted)]
    generated_text += output_char
    seed_text += output_char
    seed_text = seed_text[1:]

print(generated_text)

tokenizer.index_word[np.argmax(predicted)]