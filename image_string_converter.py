import base64
"""
# Code to get string of image
with open("./test-images/AdidasBlueShoe.jpg", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    print(str)

"""
def get_image_from_string(imageStr, image_name):
    imgdata = base64.b64decode(imageStr)
    # filename = 'some_image.jpg'
    with open(image_name, 'wb') as f:
        f.write(imgdata)
