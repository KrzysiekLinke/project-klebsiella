import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os,sys
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error
import glob
from PIL import Image
from keras.preprocessing import image
import pickle
from numpy import save

#Have you already processed the files? True/False
#default is False
#downloaded_boolean = True

#If downloaded_boolean == False. Specify the path where the data is saved.
#path = "C:\\Users\\UserName\\restOfPathToData
#path = "C:\\Users\\Joep\\Documents\\VU\\Pobp\\Data"
#Specify the path where to save the processed data. This makes it easier to load the data later.
#pathToSave = "C:\\Users\\Joep\\Documents\\VU\\Pobp"

#If downloaded_boolean == True
#pathSaved = "C:\\Users\\Joep\\Documents\\VU\Pobp"

def read_process_data(boolean, path_name, picklePath):
    if boolean == False:
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
                infected_set = np.zeros((2500,(size[0] * size[1] * 3)))
                infected_label = np.zeros((2500))
                #print(infected_set.shape)
            elif label== 0 :
                n = len(os.listdir(folder_path))
                healthy_set = np.zeros((14016,(size[0] * size[1] * 3)))
                healthy_label = np.zeros(14016)
               # print(healthy_set.shape)
            for subfolder_path in glob.glob(folder):
                subfolder = str(subfolder_path) + "\\*.jpg"
                print("Reading folder: ", subfolder)
                for image_path in glob.glob(subfolder):
                    #print(image_path)
                    im = Image.open(image_path)
                    img=image.load_img(image_path, target_size=size)
                    x=image.img_to_array(img)
                    x=x.flatten()
                    x=np.expand_dims(x, axis=0)

                    if label == 1:
                        infected_set[count,:] = x
                        infected_label[count] = label
                    elif label == 0:
                        healthy_set[count,:]= x
                        healthy_label[count] = label
                    count = count +1
            label=label-1
        #print(healthy_label)
        infected = pd.DataFrame(infected_set)
        dataset = infected.append(pd.DataFrame(healthy_set))
        #print(infected_label.shape)

        labels = (np.append(infected_label, healthy_label))

        #Save dataframes to pickle
        dataset.to_pickle(str(picklePath) + "/Processed_data.pkl")
        labels.tofile((str(picklePath) + "/Processed_labels.csv"))

    else:
        dataset = pd.read_pickle(str(path_name) + "/Processed_data.pkl")
        #print(dataset.shape)
        labels = np.fromfile(str(path_name) + "/Processed_labels.csv")
        #print(labels.shape)

    return dataset, pd.array(labels)

#Read and process the data. Specify the path to the folder with both datasets below.
#dataset, labels = read_process_data(path, pathToSave)
#print(dataset.shape)


