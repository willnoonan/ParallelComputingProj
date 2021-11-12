import numpy as np
from PIL import Image
from utility import timeit
import concurrent.futures
from imagetools import simple_boxblur
import os

image_path = r"images"

class Band:
    def __init__(self, band_data):
        self.band_data = np.array(band_data, dtype=int)
        self.shape = self.band_data.shape

    @timeit(ndigits=2)
    def simple_boxblur(self):
        return simple_boxblur(self.band_data)


img = Image.open(os.path.join(image_path, "pinkflower.jpg"))
r_band, g_band, b_band = img.split()
np_bands = dict()
np_bands["red"] = Band(r_band)
np_bands["green"] = Band(g_band)
np_bands["blue"] = Band(b_band)


def multithread():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # futures = [executor.submit(band.simple_boxblur) for band in band_np_arrs]
        futures = {band_name:executor.submit(band_obj.simple_boxblur) for band_name, band_obj in np_bands.items()}
        for _ in concurrent.futures.as_completed(futures.values()):
            pass
    return futures

futures = multithread()
new_img_data = list(zip(futures["red"].result().result,
                        futures["green"].result().result,
                        futures["blue"].result().result))

new_img = Image.new("RGB", np_bands["red"].shape[::-1])
new_img.putdata(new_img_data)
new_img.save(os.path.join(image_path, 'my_boxblurred_pinkflower.png'))

band_runtimes = [f.result().runtime for f in futures.values()]
print(f"Serial runtime: {sum(band_runtimes)}")
print(f"Concurrent runtime: {max(band_runtimes)}")
