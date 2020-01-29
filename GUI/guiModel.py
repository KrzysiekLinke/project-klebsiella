import tensorflow as tf
from tensorflow.keras import models
import glob
from keras.preprocessing import image
import numpy as np
import pathlib

def readImages(folderPath):

    tensorList = np.zeros((len(glob.glob(folderPath + "/*")),32,32,3))

    for i,image_path in enumerate(glob.glob(folderPath + "/*")):
        img = image.load_img(image_path, target_size=(32,32))
        tensorList[i,:,:,:] = image.img_to_array(img)

    return tensorList


def predictInfection(folderPath):

    data = readImages(folderPath)

    #dataScaled = data.astype('float32')
    #dataScaled /= 255

    model = tf.keras.models.load_model(str(pathlib.Path(__file__).parent.resolve()) + '/CNN_with_weights.h5')

    return [model.predict(data), model.predict_classes(data)]
