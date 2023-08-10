
from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import pytesseract
#To take pytesseract into your path

pytesseract.pytesseract.tesseract_cmd = r'path'

import requests     #if we want to do it without downloading the image

app = Flask(__name__)

@app.route("/scrape/<path:image_url>")

def scrape_image_text(image_url):
    response = requests.get(image_url)          #From requests-> it requests for image_url getting
    image = Image.open(BytesIO(response.content))   #open image content using PIL
    text = pytesseract.image_to_string(image)  #It will scrape images text

    results = {
        "image_url":image_url,
        "text":text
    }
    
    return jsonify(results)

#For running the program on the Wbpage
if(__name__=="__main__"):
    app.run(debug=True)