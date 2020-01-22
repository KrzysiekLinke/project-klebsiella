import pandas as pd
import numpy as np
import glob
from keras.preprocessing import image
import tensorflow as TF
import torch
from torchvision.transforms.functional import to_tensor

#pathFile = 'C:/Users/Marije/PycharmProjects/test/assets/Data'
pathFile = '/home/tim/Desktop/Current Courses/OBP/project-klebsiella/Data/readImages'

size = (32, 32)
datasetImages = pd.DataFrame(columns = ['Image', 'Label'])

for folder_path in glob.glob(str(pathFile) + "/*"):
    print("folder_path")
    label = 1 if ('Infected' in folder_path) else 0

    for subFolder in glob.glob(folder_path + "/*"):
        lastElement = subFolder.split("\\")[-1]
        plantType = lastElement.split("_")[0]
        className = lastElement.replace(plantType + "_", "")

        for image_path in glob.glob(subFolder + "/*"):
            img=image.load_img(image_path, target_size=size)
            datasetRow = pd.Series({'Image' : to_tensor(img), 'Label' : label, 'PlantType' : plantType, 'ClassName' : className})
            datasetImages = datasetImages.append(datasetRow, ignore_index = True)

#datasetImages.to_pickle(str('C:/Users/Marije/PycharmProjects/test/assets/Data') + "/Prescriptive_data_nn.pkl")
print("DUUURT TE LANG")
datasetImages.to_pickle(str('/home/tim/Desktop/Current Courses/OBP/project-klebsiella/Data') + "/Prescriptive_data_nn.pkl")