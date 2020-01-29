# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 12:46:09 2020

@author: daans
"""

import pandas as pd
import numpy as np

import random
import os,sys
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error
import glob
from PIL import Image
from tensorflow.keras.preprocessing import image
import pickle
from numpy import save


def read_process_data(path_name):
    path = str(path_name) + "/*"
    size = (32, 32)
    label = 1

    for folder_path in glob.glob(path):
        count = 0
        folder = str(folder_path) + "\\*"
        print("Reading folder: ", folder)
        #print(folder)
        if label == 1 :
            #print(folder_path)
            n = len(os.listdir(folder_path))
            infected_set = np.zeros((2500,32,32,3))
            infected_label = np.zeros((2500))
            #print(infected_set.shape)
        elif label== 0 :
            healthy_set = np.zeros((14016,32,32,3))
            healthy_label = np.zeros(14016)
            # print(healthy_set.shape)
        for subfolder_path in glob.glob(folder):
            subfolder = str(subfolder_path) + "\\*.jpg"
            print("Reading folder: ", subfolder)
            for image_path in glob.glob(subfolder):
                #print(image_path)
                img=image.load_img(image_path, target_size=size)
                x=image.img_to_array(img)
                ##x=x.flatten()
                ##x=np.expand_dims(x, axis=0)
                if label == 1:
                    infected_set[count,:,:,:] = x
                    infected_label[count] = label
                elif label == 0:
                    healthy_set[count,:,:,:]= x
                    healthy_label[count] = label
                count = count +1
        label=label-1
    #print(healthy_label)
    print(infected_set.shape)
    print(healthy_set.shape)
    print(infected_set[:1])
    ##infected = pd.DataFrame(infected_set)
    ##dataset = infected.append(pd.DataFrame(healthy_set))
    #print(infected_label.shape)
    dataset=(np.append(infected_set, healthy_set, axis=0))
    labels = (np.append(infected_label, healthy_label))
    print(dataset.shape)
    return dataset, pd.array(labels)

#Read and process the data. Specify the path to the folder with both datasets below.
#dataset, labels = read_process_data(path, pathToSave)
#print(dataset.shape)


