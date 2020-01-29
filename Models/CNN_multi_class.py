# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:20:33 2020

@author: daans
"""

import tensorflow as tf
from tensorflow.keras import models, layers, metrics, callbacks, optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
import pandas as pd
import numpy as np
pathFile = str(Path(__file__).parent.parent.resolve()) + "/Data/readImages"
from sklearn.model_selection import train_test_split
from data_CNN_multi_class import read_process_data
from sklearn.metrics import confusion_matrix, precision_score, recall_score,roc_curve
from matplotlib import pyplot as plt
import pickle
import math
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import utils


dataset, labels = read_process_data()
labels=np.asarray(labels)
print(dataset.shape)
print(labels.shape)


# encode class values as integers
encoder = LabelEncoder()
encoder.fit(labels)
encoded_Y = encoder.transform(labels)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = utils.to_categorical(encoded_Y)

x_train, x_test, y_train, y_test = train_test_split(dataset,  dummy_y, test_size=0.3, random_state=666)
print(x_train.shape)
print(y_train)

## making model
model = models.Sequential()
## first conv
model.add(layers.Conv2D(32,(3, 3),padding='same', input_shape=(32,32,3)))
model.add(layers.Activation('relu'))
model.add(layers.BatchNormalization(axis=3))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
## second conv
model.add(layers.Conv2D(64,(3, 3),padding='same'))
model.add(layers.Activation('relu'))
model.add(layers.BatchNormalization(axis=3))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
## third conv
model.add(layers.Conv2D(128,(3, 3),padding='same'))
model.add(layers.Activation('relu'))
model.add(layers.BatchNormalization(axis=3))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
## fourth conv
model.add(layers.Conv2D(256,(3, 3),padding='same'))
model.add(layers.Conv2D(256,(3, 3),padding='same'))
model.add(layers.Activation('relu'))
model.add(layers.BatchNormalization(axis=3))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
## fifth conv
model.add(layers.Conv2D(512,(3, 3),padding='same'))
model.add(layers.Conv2D(512,(3, 3),padding='same'))
model.add(layers.Activation('relu'))
model.add(layers.BatchNormalization(axis=3))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
##AVG pool and linear
model.add(layers.AveragePooling2D(strides=(1,1),padding='same'))
model.add(layers.Flatten())
model.add(layers.Dense(15, activation='softmax', input_dim=512))
##model.add(layers.Dense(1,activation='sigmoid'))
model.summary()
##adam=optimizers.Adam(lr=0.003)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


history=model.fit(x_train, y_train,batch_size=500 ,epochs=20, validation_split =0.2)
 


loss, acc = model.evaluate(x_test, y_test, verbose=0)
print('Test Accuracy: %.3f' % acc)
print('Test loss: %.3f' % loss)
##print(x_test[10,:,:,:])

plt.title('Learning Curves')
plt.xlabel('Epoch')
plt.ylabel('Cross Entropy')
plt.plot(history.history['loss'], label='train')

plt.plot(history.history['val_loss'], label='val')
plt.legend()
plt.show()
loss_curve=history.history['loss']
val_loss_curve=history.history['val_loss']
print(loss_curve)
acc_curve=history.history['accuracy']
val_acc_curve=history.history['val_accuracy']
print(acc_curve)

with open('C:\\Users\\daans\\Documents\\VU\\OBP\\models\\plots\\loss_acc_CNN_weights2', 'wb') as f:
    pickle.dump([loss_curve, acc_curve, val_loss_curve, val_acc_curve], f)
## accuracy
plt.plot(history.history['accuracy'], label='train')
plt.plot(history.history['val_accuracy'], label='val')
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
##save the model
models.save_model(model,"C:\\Users\\daans\\Documents\\VU\\OBP\\models\\CNN_multi_class.h5")



