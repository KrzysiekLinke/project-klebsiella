import pandas as pd
import numpy as np
import glob
from pathlib import Path
from tensorflow.keras.preprocessing import image

pathFile = str(Path(__file__).parent.parent.resolve()) + "/Data/readImages"

size = (32, 32)
datasetImages = pd.DataFrame(columns = ['Image', 'Label'])

for folder_path in glob.glob(str(pathFile) + "/*"):
    print("Reading folder: ", folder_path)
    label = 1 if ('Infected' in folder_path) else 0

    for subFolder in glob.glob(folder_path + "/*"):

        print("Reading subfoulder: ", subFolder)
        for image_path in glob.glob(subFolder + "/*")            :

            img=image.load_img(image_path, target_size=size)
            x = image.img_to_array(img)
            x = x.flatten()
            x = np.expand_dims(x, axis = 0)

            datasetRow = pd.Series({'Image' : x, 'Label' : label})
            datasetImages = datasetImages.append(datasetRow, ignore_index = True)

print(datasetImages.shape)
pathFile = str(Path(__file__).parent.parent.resolve()) + "/Data/Pickle_array/Processed_data.pkl"
datasetImages.to_pickle(pathFile)