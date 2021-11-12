from PIL import Image, ImageFilter

before = Image.open("../images/flower.png")
after = before.filter(ImageFilter.BoxBlur(5))
after.save("blurred_flower.png")