from PIL import Image

img = Image.open("../images/flower.png")
img = img.convert("RGB")
img_data = img.getdata()

# Very cool site: https://ciechanow.ski/color-spaces/

target_rgb_min = 190
target_rgb_max = 256
new_rgb = (50, 0, 204)

def replace_img_colors():
    new_image = []
    for pxl_rgb in img_data:
        rgb_in_range = [target_rgb_min <= val <= target_rgb_max for val in pxl_rgb]
        if all(rgb_in_range):
            new_image.append(new_rgb)
        else:
            new_image.append(pxl_rgb)
    return new_image




# update image data
# img.putdata(replace_img_colors())

# save new image
# img.save("flower_image_altered.png")
if __name__ == "__main__":
    print("hello")
