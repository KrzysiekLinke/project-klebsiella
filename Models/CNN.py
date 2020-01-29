# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:43:34 2020

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
from data_CNN import read_process_data
from sklearn.metrics import confusion_matrix, precision_score, recall_score,roc_curve
from matplotlib import pyplot as plt
import pickle
import math

path = "C:\\Users\\daans\\Documents\\VU\\OBP\\data\\testdata" ## fodler where data is stored in 2 maps with bacerial spots and non bacterial spots


dataset, labels = read_process_data(path)
labels=np.asarray(labels)
print(dataset.shape)
print(labels.shape)



x_train, x_test, y_train, y_test = train_test_split(dataset,  labels, test_size=0.3, random_state=666)
print(x_train.shape)


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
##model.add(layers.Dense(15, activation='linear', input_dim=512))
model.add(layers.Dense(1,activation='sigmoid'))
model.summary()
##adam=optimizers.Adam(lr=0.003)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
## using weight
class_weights = {0:0.15,1:0.85}
## fit model

history=model.fit(x_train, y_train,batch_size=500 ,epochs=20, validation_split =0.2, class_weight=class_weights)



loss, acc = model.evaluate(x_test, y_test, verbose=0)
print('Test Accuracy: %.3f' % acc)
print('Test Loss: %.3f' % loss)
test_predict_proba=model.predict(x_test) ## for probability
test_predict=model.predict_classes(x_test) ## for class

print(test_predict)
print(test_predict_proba)
print(type(test_predict))
test_predict=test_predict.flatten()

print(pd.Series(test_predict).value_counts())
print(pd.Series(y_test).value_counts())
cm=confusion_matrix(y_test, test_predict)
precision=precision_score(y_test, test_predict)
recall=recall_score(y_test, test_predict)
print(precision, recall)
print(cm)
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
##print(test_predict2)
models.save_model(model,"C:\\Users\\daans\\Documents\\VU\\OBP\\models\\CNN_with_weights.h5")



