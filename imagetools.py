import numpy as np

def simple_boxblur(img_data):
    """Box blur algorithm with radius = 1."""
    img_data = np.array(img_data, dtype=int)
    img_shape = img_data.shape
    h, w = img_shape
    new_img_data = []
    for i in range(0, h):
        # Edge check, above and below:

        above = i - 1
        if above < 0:
            above = 0

        below = i + 1
        if below > h - 1:
            below = h - 1

        for j in range(0, w):
            # Edge check, left and right:
            left = j - 1
            if left < 0:
                left = 0

            right = j + 1
            if right > w - 1:
                right = w - 1

            # take average of 3-by-3 box around current pixel:
            sum = (img_data[i][j]
                   + img_data[i][left] + img_data[i][right]
                   + img_data[above][j] + img_data[above][left]
                   + img_data[above][right] + img_data[below][j]
                   + img_data[below][left] + img_data[below][right])
            avg = round(sum / 9)
            new_img_data.append(avg)
    return new_img_data


def simple_boxblur_V2(img_data):
    """
    Second version of box blur algorithm with radius = 1.
    Meant to be a stepping stone to a method with variable radius.
    """
    radius = 1
    box_size = (2 * radius + 1) ** 2
    img_data = np.array(img_data, dtype=int)
    img_shape = img_data.shape
    h, w = img_shape
    new_img_data = []
    for row in range(0, h):
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
