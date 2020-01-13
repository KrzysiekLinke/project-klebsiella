import os
import pathlib
import pandas as pd


def read_files(**kwargs):
    data = pd.DataFrame([])

    uploadedDirectory = kwargs.get('imageDirectory', None)
    image_directory = str(pathlib.Path(__file__).parent.resolve()) + '/assets/images/'

    if uploadedDirectory is not None:
        image_directory = uploadedDirectory

    for i,f in enumerate(os.listdir(image_directory)):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):

            data = data.append(pd.DataFrame({'id': i, 'leaf': f}, index=[0]), ignore_index=True)

    return data

def findFilePath(filename):

    for root, dirs, files in os.walk(".", topdown = False):
        if filename in files:
            return os.path.join(root, filename)

    return None






