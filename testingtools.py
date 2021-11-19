from imagetools import *
from PIL import Image
import concurrent.futures
import os
import numpy as np

def blurimageby(method):
    image_path = r"images"
    img = Image.open(os.path.join(image_path, "pinkflower.jpg"))
    r_band, g_band, b_band = img.split()
    bands = {"red": r_band, "green": g_band, "blue": b_band}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {band_name: executor.submit(method, band) for band_name, band in bands.items()}
        for _ in concurrent.futures.as_completed(futures.values()):
            pass
    new_img_data = list(zip(futures["red"].result(),
                            futures["green"].result(),
                            futures["blue"].result()))
    new_img = Image.new("RGB", np.array(r_band, dtype=int).shape[::-1])
    new_img.putdata(new_img_data)
    new_img.save(os.path.join(image_path, f'{method.__name__}_pinkflower.png'))
    return futures





