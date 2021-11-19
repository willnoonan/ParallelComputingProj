from PIL import Image
import numpy as np

rgb_p1 = np.array([0]*3)
rgb_p2 = np.array([256]*3)

m = rgb_p2 - rgb_p1

def get_t(point):
    point = np.array(point)
    return (point - rgb_p1)/m

def point_on_3Dline(point):
    return len(set(get_t(point))) == 1

def point_on_3Dline_segment(point):
    t = get_t(point)
    return point_on_3Dline(point) and (0 <= t[0] <= 1)

img = Image.open("../images/flower.png")
img = img.convert("RGB")
img_data = img.getdata()
print(f"Image size: {img.size}")

target_rgb_range = list(range(180, 256))
new_rgb = (204, 0, 204)

new_image = []
for pxl_rgb in img_data:
    # change all white (also shades of whites)
    # pixels to yellow
    # pxl_r, pxl_g, pxl_b = pxl_rgb
    # on_line = point_on_3Dline_segment(pxl_rgb)
    rgb_in = [val in target_rgb_range for val in pxl_rgb]
    if all(rgb_in):
    # if on_line:
        new_image.append(new_rgb)
    else:
        new_image.append(pxl_rgb)

# update image data
img.putdata(new_image)

# save new image
img.save("flower_image_altered.png")

