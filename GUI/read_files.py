import os
import pathlib
import pandas as pd


def read_files():
    data = pd.DataFrame([])

    image_directory = str(pathlib.Path(__file__).parent.parent.resolve()) + '/images/'
    i = 0
    for f in os.listdir(image_directory):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            f=image_directory+f
            data = data.append(pd.DataFrame({'id': i, 'path': f}, index=[0]), ignore_index=True)
            i = i + 1
    return data



