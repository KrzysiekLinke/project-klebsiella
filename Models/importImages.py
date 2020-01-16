import pandas as pd
import numpy as np
import glob
from keras.preprocessing import image
import tensorflow as TF
import torch
from torchvision.transforms.functional import to_tensor

pathFile = '/home/tim/Desktop/OBP/project-klebsiella/Data/readImages'

size = (32, 32)
datasetImages = pd.DataFrame(columns = ['Image', 'Label'])

for folder_path in glob.glob(str(pathFile) + "/*"):

    label = 1 if ('Infected' in folder_path) else 0

    for subFolder in glob.glob(folder_path + "/*"):

        for image_path in glob.glob(subFolder + "/*"):

            img=image.load_img(image_path, target_size=size)
            datasetRow = pd.Series({'Image' : to_tensor(img), 'Label' : label})
            datasetImages = datasetImages.append(datasetRow, ignore_index = True)

datasetImages.to_pickle(str('/home/tim/Desktop/OBP/project-klebsiella/Data/Pickle') + "/Processed_data_nn.pkl")
