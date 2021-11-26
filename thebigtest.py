import numpy as np
from PIL import Image
from utility import timeit
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import itertools as it
import os

image_path = "images"

class Band:
    """Class to hold color-band data and associated info."""
    def __init__(self, band_data):
        self.band_data = np.array(band_data, dtype=int)
        self.shape = self.band_data.shape

    @timeit(ndigits=2)
    def boxblur_band_by_chunks(self, nchunks=1, radius=1):
        """
        Blurs pixel data for the color band. If nchunks > 1, the pixel matrix is split into nchunks, where each
        chunks is its own process.
        :param nchunks: number of chunks to split the pixel matrix into, which is also the number of processes to use
        :param radius: radius of the box blur
        :return: list of ints
        """
        if nchunks == 1:
            return self.boxblur(radius=radius)

        band_data = self.band_data
        h, _ = band_data.shape
        chunk_indices = np.array_split(range(h), nchunks) # list of lists
        futures = dict()
        with ProcessPoolExecutor() as executor:
            for i, cl in enumerate(chunk_indices):
                row_start = cl[0]
                row_stop = cl[-1] + 1
                futures[i] = executor.submit(self.boxblur, radius=radius, row_range=(row_start, row_stop))
            for _ in as_completed(futures.values()):
                pass
        sorted_futures = {key: futures[key].result() for key in sorted(futures.keys())}
        chained_results = list(it.chain(*sorted_futures.values()))
        return chained_results


    def boxblur(self, radius=1, row_range=None):
        """
        Box-blur method with variable radius.
        """
        if radius < 0:
            raise ValueError("radius must be >= 0")

        if row_range:
            if not isinstance(row_range, tuple):
                raise TypeError("row_range must of type tuple")
            if len(row_range) != 2:
                raise ValueError("row_range must be of length 2")

        img_data = self.band_data  # band_data is already np.array of dtype int
        box_size = (2 * radius + 1) ** 2
        h, w = img_data.shape
        row_start = 0
        row_end = h
        if row_range:
            row_start = row_range[0]
            row_end = row_range[1]
        new_img_data = []
        for row in range(row_start, row_end):
            for col in range(0, w):
                # Determine indices for box's top left corner (prefix a) and bottom right corner (prefix b)
                ai = row - radius  # row index of box top left corner
                aj = col - radius  # col index of box top left corner
                bi = row + radius  # row index of box bottom right corner
                bj = col + radius  # col index of box bottom right corner
                sum = 0
                for br in range(ai, bi + 1):
                    for bc in range(aj, bj + 1):
                        i = br  # copy box row loop var into new var
                        j = bc  # copy box col loop var into new var
                        if i < 0:
                            i = 0
                        if i > h - 1:
                            i = h - 1
                        if j < 0:
                            j = 0
                        if j > w - 1:
                            j = w - 1
                        sum += img_data[i][j]  # use i and j values to get the matrix value
                avg = round(sum / box_size)
                new_img_data.append(avg)
        return new_img_data


class MyImage:
    def __init__(self):
        # Create Image object from the input image:
        img = Image.open(os.path.join(image_path, "pinkflower.jpg"))
        r_band, g_band, b_band = img.split()  # get each color band out of the image
        # Create a dict to store the Band objects for each color band:
        bands = dict()
        bands["red"] = Band(r_band)
        bands["green"] = Band(g_band)
        bands["blue"] = Band(b_band)
        self.bands = bands
        self.width = img.width
        self.height = img.height

    def boxblurImageByChunks(self, nchunks=1, radius=1):
        """
        Blurs each band separately as their own process. Returns after each band has finished.
        Timing this only lets you know the parallel runtime, but it's not accurate for some reason.
        :returns dict of band color, Wrap object, which
        """
        bands = self.bands
        with ProcessPoolExecutor() as executor:
            futures = {band_color: executor.submit(band_obj.boxblur_band_by_chunks, nchunks=nchunks, radius=radius) for band_color, band_obj in
                       bands.items()}
            for _ in as_completed(futures.values()):
                pass
            blurred_bands = {band_color: future.result() for band_color, future in futures.items()}
        return blurred_bands


def sequential():
    """
    Made this use multiprocessing when running performance tests, but it doesn't work.
    Results in much larger runtimes. Maybe because there are too many processes.
    :return:
    """
    myimg = MyImage()
    blurred_image = myimg.boxblurImageByChunks(nchunks=1, radius=1)
    total = 0
    for band in blurred_image.values():
        total += band.runtime
    return total

def main():
    myimg = MyImage()
    nruns = 5
    sequential = []

    data = []
    import csv
    with open("ParallelRuntimes.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["radius", "nchunks", "runtime"])
        for radius in [1,2,3]:
            for nchunks in [1,2,3,4,5,6]:
                parallel = []
                for run in range(nruns):
                    blurred_image = myimg.boxblurImageByChunks(nchunks=nchunks, radius=radius)
                    band_runtimes = [band.runtime for band in blurred_image.values()]
                    parallel.append(max(band_runtimes))
                mean_p_runtime = round(np.mean(parallel), 2)
                writer.writerow([radius, nchunks, mean_p_runtime])


    # print(data)

    # print(f"Avg, Std Sequential Runtime: {round(np.mean(sequential), 2), round(np.std(sequential), 2)}")
    # print(f"Avg Parallel Runtime: {round(np.mean(parallel), 2), round(np.std(parallel), 2)}")

    # nruns = 10
    # totalruntime = 0
    # for x in range(nruns):
    #     blurred_image = myimg.boxblurImageByChunks(nchunks=2, radius=1)
    #     totalruntime += blurred_image.runtime

    # with ProcessPoolExecutor() as executor:
    #     processes = [executor.submit(myimg.boxblurImageByChunks, nchunks=1, radius=1) for _ in range(nruns)]
    #     for p in as_completed(processes):
    #         totalruntime += p.result().runtime

    # print(f"Avg Runtime: {round(totalruntime/nruns, 2)}")

    # # Compare the serial run time to the parallel run time:
    # band_runtimes = [band.runtime for band in blurred_bands.values()]
    # print(f"Serial runtime: {round(sum(band_runtimes), 2)}")  # sum the run times to get the serial run time
    # print(f"Concurrent runtime: {max(band_runtimes)}")  # the parallel run time is the max of the run times


# The following prevents RuntimeError for 'spawn' and 'forkserver' start_methods:
if __name__ == '__main__':
    main()