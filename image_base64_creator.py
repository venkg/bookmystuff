import base64

# Code to get string of image
with open("./test-images/AdidasBlueShoe.jpg", "rb") as imageFile:
    str = base64.b64encode(imageFile.read())
    print(str)

