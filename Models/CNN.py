import tensorflow as tf
from tensorflow.keras import models, layers

model = models.Sequential()
## first conv
model.add(layers.Conv2D(32,(3, 3),padding='same', input_shape=(32,32,3)))
model.add(layers.BatchNormalization(axis=3))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
## second conv
model.add(layers.Conv2D(64,(3, 3),padding='same'))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
## third conv
model.add(layers.Conv2D(128,(3, 3),padding='same'))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
## fourth conv
model.add(layers.Conv2D(256,(3, 3),padding='same'))
model.add(layers.Conv2D(256,(3, 3),padding='same'))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
## fifth layer
model.add(layers.Conv2D(512,(3, 3),padding='same'))
model.add(layers.Conv2D(512,(3, 3),padding='same'))
model.add(layers.MaxPooling2D(strides=(2,2), padding='same'))
##AVG pool and linear
model.add(layers.AveragePooling2D(strides=(1,1),padding='same'))
model.add(layers.Dense(15, activation='linear', input_dim=512))
## normalization
model.add(layers.BatchNormalization(axis=3))

model.summary()

