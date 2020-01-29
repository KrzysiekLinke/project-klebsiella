# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:24:53 2020

@author: daans
"""

import pandas as pd
import numpy as np
import glob
from tensorflow.keras.preprocessing import image
from pathlib import Path
def read_process_data():
    pathFile = 'C:\\Users\\daans\\Documents\\VU\\OBP\\data\\testdata'
    
    size = (32, 32)
    datasetImages = np.zeros((16516, 32, 32, 3))
    ##classes = [14016]
    labels = np.zeros((16516))
    count, label = 0, 0
    
    for folder_path in glob.glob(str(pathFile) + "/*"):
        print("Reading folder: ", folder_path)
        for subFolder in glob.glob(folder_path + "/*"):
            print("Reading subfoulder: ", subFolder)
            print(subFolder.split('\\', -1)[-1], label)
            Class = subFolder.split('\\', -1)[-1]
            for image_path in glob.glob(subFolder + "/*"):
                img=image.load_img(image_path, target_size=size)
                x = image.img_to_array(img)
                
                datasetImages[count, :, :, :] = x
                ##classes[count] = str(Class)
                labels[count] = label
                count = count+1
            label =label+ 1
    return datasetImages, labels       
            