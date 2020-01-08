import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os,sys
path="C:\\Users\\daans\\Documents\\VU\\OBP\\data\\plant_leaf_dataset"
os.chdir(path)

import glob
import imageio
from PIL import Image

i=1
##for image_path in glob.glob("C:\\Users\\daans\\Documents\\VU\\OBP\\data\\plant_leaf_dataset\\Pepperbell_bacterial_spot\\*.jpg"):
    ##im = imageio.imread(image_path)
    ##print (im.shape)
    ##print (im.dtype)
    ##im.resize(size)
    ##im.save(i,"jpg")
   ## i=i+1
size=(32, 32)
for image_path in glob.glob("C:\\Users\\daans\\Documents\\VU\\OBP\\data\\plant_leaf_dataset\\Pepperbell_bacterial_spot\\*.jpg"):
    im = Image.open(image_path)
    width,height = im.size
    x=np.array(im)
    print(x[1,1,1])
    out=im.resize(size)
    ##out.save(str(i) + ".jpg")
    i=i+1

