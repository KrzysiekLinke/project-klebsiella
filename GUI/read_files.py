import os
import pandas as pd
from pathlib import Path


def read_files(image_directory):
    data = pd.DataFrame([])
    error3 = False;

    for i,f in enumerate(os.listdir(image_directory)):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):

            data = data.append(pd.DataFrame({'id': i, 'leaf': f}, index=[0]), ignore_index=True)

    if data.empty:
        error3 = True


    return data, error3

def findFilePath(filename):
    projectPath = Path(os.getcwd()).parent

    for root, dirs, files in os.walk(projectPath):
        if filename in files:
            return Path(os.path.join(root, filename))

    return None






