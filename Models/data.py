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

size=(32, 32)
label=1


#file_count=os.listdir("C:\\Users\\daans\\Documents\\VU\\OBP\\data\\plant_leaf_dataset\\Pepperbell_bacterial_spot")
#n=len(file_count)
#train_set=np.zeros(((size[0]*size[1]*3),n))
for folder_path in glob.glob("C:\\Users\\Joep\\Documents\\VU\\Pobp\\Data\\*"):
    count=0
    folder = str(folder_path) + "\\*.jpg"
    print(folder)
    if label == 1 :
        print(folder_path)
        n = len(os.listdir(folder_path))
        infected_set = np.zeros((n,(size[0] * size[1] * 3)))
        infected_label = np.zeros((n))
        #print(infected_set.shape)
    elif label== 0 :
        n = len(os.listdir(folder_path))
        healthy_set = np.zeros((n,(size[0] * size[1] * 3)))
        healthy_label = np.zeros(n)
       # print(healthy_set.shape)
    for image_path in glob.glob(folder):
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
dataset = infected.append(pd.DataFrame(healthy_set))/255
#print(infected_label.shape)

labels = pd.array(np.append(infected_label, healthy_label))
#print(labels.shape)
#print(dataset.shape)

#Test-train split
x_train, x_test, y_train, y_test = train_test_split(dataset,  labels, test_size=0.3, random_state=666)

#Logistic Regression
clf = LogisticRegression(max_iter=1000).fit(x_train,y_train)
predict = clf.predict(x_test)
print(clf.score(x_test, y_test))
print(mean_absolute_error(y_test, predict))


