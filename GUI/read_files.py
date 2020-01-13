import os
import pathlib
import pandas as pd
from PIL import Image

def read_files():
    data = pd.DataFrame([])

    image_directory = str(pathlib.Path(__file__).parent.resolve()) + '/assets/images/'
    i = 0
    for f in os.listdir(image_directory):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            try:
                im = Image.open(image_directory+f)
                im.verify()  # I perform also verify, don't know if he sees other types o defects
                im.close()  # reload is necessary in my case
                im = Image.open(image_directory+f)
                im.transpose(Image.FLIP_LEFT_RIGHT)
                im.close()
                data = data.append(pd.DataFrame({'id': i, 'leaf': f}, index=[0]), ignore_index=True)
                i = i + 1
            except:
                print("File " + f + " is not an Image.")
    return data




