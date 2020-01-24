
import os
from flask import Flask
from flask import request
from image_predict import predict_image_class
from image_string_converter import get_image_from_string
from flask import jsonify
from datetime import datetime


LABEL_PATH = "./tmp/output_labels.txt"

app = Flask(__name__)

@app.route('/hello')
def helloIndex():
    return 'Hello from Book My Stuff!'

@app.route('/product')
def searchProduct():
    image_name = request.args.get('name')
    predicted_class = ""
    if image_name.lower().endswith(('.jpg', '.jpeg')):
        # predict the class of the image
        predicted_class = predict_image_class("./test-images/"+image_name, LABEL_PATH)
    else:
        predicted_class = 'File must be a jpeg image.'
    return jsonify(predicted_class)

@app.route('/product', methods = ['POST'])
def search_product():
    if request.method == 'POST':
        # get current time and append to temp file name
        current_time = datetime.now().strftime("%d%m%Y%H%M%S")
        image_name = 'temp_image_' + current_time + '.jpg'
        product_image = request.form.get('product_image')
        # save string to image file
        get_image_from_string(product_image, image_name)
        # predict the class of the image
        predicted_class = predict_image_class(image_name, LABEL_PATH)
        if os.path.exists(image_name):
            os.remove(image_name)
        return jsonify(predicted_class)

app.run(host='0.0.0.0', port= 81)

"""
Comment above line and uncomment below to dockerize
"""

"""
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)
"""
