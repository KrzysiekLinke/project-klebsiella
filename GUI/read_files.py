import os
import pathlib
import pandas as pd


def read_files():
    data = pd.DataFrame([])

    image_directory = str(pathlib.Path(__file__).parent.resolve()) + '/assets/images/'
    i = 0
    for f in os.listdir(image_directory):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):

            data = data.append(pd.DataFrame({'id': i, 'leaf': f}, index=[0]), ignore_index=True)
            i = i + 1
    return data




