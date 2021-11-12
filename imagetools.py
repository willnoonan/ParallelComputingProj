import numpy as np

def simple_boxblur(img_data):
    # Radius = 1
    img_data = np.array(img_data, dtype=int)
    img_shape = img_data.shape
    h, w = img_shape
    new_img_data = []
    for i in range(0, h):
        # Edge check(A for 'above' index and B for 'below'):
        above = i - 1
        if (above < 0):
            above = 0

        below = i + 1
        if (below > h - 1):
            below = h - 1

        for j in range(0, w):
        # Edge check (L = 'left of', R = 'right of'):
            left = j - 1
            if (left < 0):
                left = 0

            right = j + 1
            if (right > w - 1):
                right = w - 1
            # Then change all your 'i-1' | 'i+i' | 'j-i' | j+1' indexes to A|B|L|R:

            # take average of 3-by-3 box around current pixel:
            avg = round((img_data[i][j]
                + img_data[i][left] + img_data[i][right]
                + img_data[above][j] + img_data[above][left]
                + img_data[above][right] + img_data[below][j]
                + img_data[below][left] + img_data[below][right]) / 9)
            new_img_data.append(avg)
    return new_img_data