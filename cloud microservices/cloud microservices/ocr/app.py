from flask import Flask,jsonify, request
from ocr import *
import base64

app = Flask(__name__)

# @app.route("/generate")
# def generate():
#     with open("ocr.jpg", "rb") as img_file:
#         bStr = base64.b64encode(img_file.read())
#         bStr = bStr.decode('ascii')
#     return jsonify({
#         "data" : bStr
#     }),200

@app.route('/getplatenum', methods = ['POST'])
def ocr():
    if request.method == "POST":
        data = request.get_json()
        b64 = data['base64']
        imgBase64 = str.encode(b64)
        imgDecoded = base64.decodestring(imgBase64)
        imgFile = open("ocr.jpg", "wb")
        try:
            imgFile.write(imgDecoded)
            texts = validateImage()
            pNum = texts[0][:-1]
            pNum = pNum.replace(" ", "-")
            os.remove("ocr.jpg")
            return jsonify({
                'code' : 200,
                'data' : {
                    "pNum" : pNum
                }
            }),200
        except Exception as e:
            print(e)
            return jsonify({
                'code' : 404,
                'status' : "base64 is invalid"
            }),404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)