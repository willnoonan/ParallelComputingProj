import numpy as np
from PIL import Image
from utility import timeit
import concurrent.futures
from imagetools import simple_boxblur
import os

image_path = r"images"

class Band:
    """Class to hold color-band data and associated info."""
    def __init__(self, band_data):
        self.band_data = np.array(band_data, dtype=int)
        self.shape = self.band_data.shape

    @timeit(ndigits=2)
    def simple_boxblur(self):
        return simple_boxblur(self.band_data)


# Create Image object from the input image:
img = Image.open(os.path.join(image_path, "pinkflower.jpg"))
r_band, g_band, b_band = img.split() # get each color band out of the image
# Create a dict to store the Band objects for each color band:
np_bands = dict()
np_bands["red"] = Band(r_band)
np_bands["green"] = Band(g_band)
np_bands["blue"] = Band(b_band)


def multithread():
    """Where the multithreading happens. I create a thread for each color band because
    they need to be blurred separately.

    :returns dict
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {band_name:executor.submit(band_obj.simple_boxblur) for band_name, band_obj in np_bands.items()}
        for _ in concurrent.futures.as_completed(futures.values()):
            pass
    return futures

# Store the completed threads in dict futures:
futures = multithread()

# Combine the blurred RGB color bands:
new_img_data = list(zip(futures["red"].result().result,
                        futures["green"].result().result,
                        futures["blue"].result().result))

# Make a new Image object with the blurred image data:
new_img = Image.new("RGB", np_bands["red"].shape[::-1]) # Image.new wants size arg as (w, h) instead of the typical (h, w)
new_img.putdata(new_img_data)
new_img.save(os.path.join(image_path, 'my_boxblurred_pinkflower.png'))

# Compare the serial run time to the parallel run time:
band_runtimes = [f.result().runtime for f in futures.values()]
print(f"Serial runtime: {sum(band_runtimes)}") # sum the run times to get the serial run time
print(f"Concurrent runtime: {max(band_runtimes)}") # the parallel run time is the max of the run times
