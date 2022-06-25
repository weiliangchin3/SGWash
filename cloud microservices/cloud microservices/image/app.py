import base64
from flask import Flask, jsonify, request
import pyrebase
import time, os

import requests

config = {
    "apiKey": "AIzaSyCeCVHV_iY0xXeTWBUiFGlvSTQturRngWU",
    "authDomain": "fil-flutter-f31f2.firebaseapp.com",
    "databaseURL": "https://fil-flutter-f31f2-default-rtdb.firebaseio.com",
    "projectId": "fil-flutter-f31f2",
    "storageBucket": "fil-flutter-f31f2.appspot.com",
    "messagingSenderId": "701218164702",
    "appId": "1:701218164702:web:f132c9d586e4a36c7ad74f"
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'code' : 200,
        'status' : "no route selected"
    }),200

# GET customer image URL
@app.route('/customerimg')
def customerImage():
    if request.method == "GET":
        custID = request.args.get("custID")
        url = storage.child('userVehicles/{}.png'.format(custID)).get_url("")
        statusCode = requests.get(url).status_code
        if statusCode == 200:
            return jsonify({
                'code' : 200,
                'data' : {
                    "link" : str(url)
                }
            }),200
        else:
            return jsonify({
                "code" : 404,
                "status" : "Customer image does not exist"
            }),404

# @app.route('/download')
# def download():
#     if request.method == "GET":
#         # jsonInput = request.get_json()
#         custID = request.args.get("custID")
#         dateTime = request.args.get("dateTime")
#         url = storage.child('jobsCompleted/{}-{}.png'.format(dateTime,custID)).get_url("")
#         # print('{}-{}.png'.format(dateTime, custID))
#         # url = storage.child('jobsCompleted/{}.png'.format(custID)).get_url("")
#         statusCode = requests.get(url).status_code
#         if statusCode == 200:
#             return jsonify({
#                 'code' : 200,
#                 "data" : {
#                     "link" : str(url)
#                 }
#             }),200

#     return jsonify({
#         'code' : 500,
#         'status' : "No image found"
#     }),500

# upload image to firebase storage
@app.route('/upload', methods = ["POST"])
def upload():
    if request.is_json:
        data = request.get_json()
        imgBase64 = data['base64']
        folderName = data['folderName']
        imgBase64 = str.encode(imgBase64)
        imgDecoded = base64.decodestring(imgBase64)
        custID = data['custID']
        newImage = open('{}.png'.format(custID), "wb")
        newImage.write(imgDecoded)
        time.sleep(3)
        try:
            # folder name is either jobsCompleted or userVehicles
            if folderName == "jobsCompleted":
                dateTime = data['dateTime']
                storage.child("{}/{}-{}.png".format(folderName,dateTime,custID)).put("{}.png".format(custID))
            else:
                storage.child("{}/{}.png".format(folderName,custID)).put("{}.png".format(custID))
            print("image uploaded")
            os.remove("{}.png".format(custID))
            return jsonify({
                "code" : 200,
                "status" : "Image uploaded"
            }),200
        except Exception as e:
            print(e)
            return jsonify({
                'code' : 500,
                'status' : "Image could not be uploaded"
            }),500
    return jsonify({
        'code' : 400,
        'stauts' : 'base64 is invalid'
    }),400 



if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")