import numpy as np
import math

from PIL import Image
import numpy
img = Image.open("../images/pinkflower.jpg")
img_rgb = img.convert("RGB")
img_rgb_data = list(img.getdata())
r, g, b = img.split()
np_img_r = np.array(r, dtype=int)
np_img_g = np.array(g, dtype=int)
np_img_b = np.array(b, dtype=int)

# print(np_img_r.shape)

# size of image:


def gaussBlur_1 (img_data, r):
    h, w = img_data.shape
    img_data = img_data.flatten()
    new_img_data = np.zeros(img_data.size)
    rs = math.ceil(r * 2.57)     # significant radius
    for i in range(h): #for(var i=0; i<h; i++)
        for j in range(w): #for(var j=0; j<w; j++) {
            val = 0
            wsum = 0
            for iy in range(i-rs, i+rs+1): #for(var iy = i-rs; iy<i+rs+1; iy++)
                for ix in range(j-rs, j+rs+1): #for(var ix = j-rs; ix<j+rs+1; ix++) {
                    x = min(w - 1, max(0, ix)) #var x = Math.min(w-1, Math.max(0, ix));
                    y = min(h - 1, max(0, iy)) #var y = Math.min(h-1, Math.max(0, iy));
                    dsq = (ix-j)*(ix-j)+(iy-i)*(iy-i) #var dsq = (ix-j)*(ix-j)+(iy-i)*(iy-i);
                    wght = math.exp( -dsq / (2*r*r) ) / (math.pi*2*r*r) #var wght = Math.exp( -dsq / (2*r*r) ) / (Math.PI*2*r*r);
                    try:
                        val += img_data[y*w+x] * wght
                    except Exception as e:
                        raise(e)
                    wsum += wght
            new_img_data[i*w+j] = round(val/wsum)
    return new_img_data



def my_box_blur(img_data):
    img_shape = img_data.shape
    h, w = img_shape
    # new_img_data = np.zeros(img_shape)
    test_arr = []
    for i in range(0, h):
        # Edge check(A for 'above' index and B for 'below'):
        above = i - 1
        if (above < 0): above = 0

        below = i + 1
        if (below > h - 1): below = h - 1
        for j in range(0, w):
        # Edge check (L = 'left of', R = 'right of'):
            left = j - 1
            if (left < 0): left = 0

            right = j + 1
            if (right > w - 1): right = w - 1
            # Then change all your 'i-1' | 'i+i' | 'j-i' | j+1' indexes to A|B|L|R:

            avg = round((img_data[i][j]
            + img_data[i][left] + img_data[i][right]
            + img_data[above][j] + img_data[above][left]
            + img_data[above][right] + img_data[below][j]
            + img_data[below][left] + img_data[below][right]) / 9)
            # new_img_data[i][j] = avg
            test_arr.append(avg)
    return test_arr

blur_data_r = my_box_blur(np_img_r)
blur_data_g = my_box_blur(np_img_g)
blur_data_b = my_box_blur(np_img_b)
new_img = list(zip(blur_data_r, blur_data_g, blur_data_b))
# print(sum(test_arr - np_img_r.flatten()))
# img_out = Image.fromarray(np_img_r,"RGB")
# img_out.save('gauss_blur_test.png')
img_out = Image.new('RGB', np_img_r.shape[::-1])
img_out.putdata(new_img)
img_out.save('gauss_blurred.png')
# print(type(np_img_r[0][0]))