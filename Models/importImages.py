import pandas as pd
import numpy as np
import glob
from tensorflow.keras.preprocessing import image

pathFile = 'C:\\Users\\Joep\\Project\\project-klebsiella\\Data\\readImages'

size = (32, 32)
datasetImages = pd.DataFrame(columns = ['Image', 'Label'])

for folder_path in glob.glob(str(pathFile) + "/*"):
    print("Reading folder: ", folder_path)
    label = 1 if ('Infected' in folder_path) else 0

    for subFolder in glob.glob(folder_path + "/*"):

        print("Reading subfoulder: ", subFolder)
        for image_path in glob.glob(subFolder + "/*"):

            img=image.load_img(image_path, target_size=size)
            datasetRow = pd.Series({'Image' : image.img_to_array(img), 'Label' : label})
            datasetImages = datasetImages.append(datasetRow, ignore_index = True)

datasetImages.to_pickle(str('C:\\Users\\Joep\\Project\\project-klebsiella\\Data\\Pickle') + "/Processed_data_nn.pkl")
#importDataset = pd.read_pickle(str('/home/tim/Desktop/OBP/project-klebsiella/Data/Pickle') + "/Processed_data_nn.pkl")