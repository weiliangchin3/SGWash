from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
apiKey = 'AIzaSyAFugfOe_LlScxjSC_GrQTI1c2R-7wmS7k'

@app.route('/validateaddress')
def index():
    location = request.args.get("pCode")
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}&components=country:SG".format(location,apiKey)
        response = requests.get(url)
        data = response.json()
        if data['status'] == "OK":
            return jsonify({
                "code" : 200,
                "status" : "Address is valid",
            }),200
        else:
                return jsonify({
                "code" : 404,
                "status" : "Address is invalid",
            }),404
    except Exception as e:
        print(e)   
    return jsonify({
                "code" : 500,
                "status" : "Unable to validate postal code"
            }),500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)