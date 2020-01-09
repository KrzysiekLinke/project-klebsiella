from Models.data import read_process_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os,sys
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import confusion_matrix
import glob
from PIL import Image
#from keras.preprocessing import image
import pickle
from numpy import save

#Have you already processed the data?
boolean = False

#If you have already processed the data, specify the path where the datasets are. Otherwise
#specify the path where the unprocessed data is and where you want to save the processed data.
path = "C:\\Users\\Joep\\Documents\\VU\\Pobp\\Data"
pathToSave = "C:\\Users\\Joep\\Documents\\VU\\Pobp"

dataset, labels = read_process_data(boolean, path, pathToSave)

#Standardize data
sd_dataset = dataset/255

#Test-train split
x_train, x_test, y_train, y_test = train_test_split(sd_dataset,  labels, test_size=0.3, random_state=34)

#Data distribution
#series = pd.Series(labels)
#print(series.value_counts())
#plt.bar(labels, )
#plt.show()

#Logistic Regression
#print("Fitting logistic regression")
#clf = LogisticRegression(max_iter=500).fit(x_train,y_train)
#predict = clf.predict(x_test)
#print(type(predict))
#print(pd.Series(predict).value_counts())
#print(pd.DataFrame(predict).count())
#print("Logistic regression accuracy is: ", clf.score(x_train, y_train))
#print("Logistic regression MAE is: ", mean_absolute_error(y_test, predict))
#print(confusion_matrix(y_test, predict))
