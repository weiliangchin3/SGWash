import facebook as fb 
import os
from flask import Flask, request, jsonify, redirect, flash
import urllib.request
#from app import app
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
import base64
import time


app = Flask(__name__)
CORS(app)
access_token = ""

#user_access_token = 'USER_ACCESS_TOKEN' # initially generated client-side
app_id = '' # found at developer.facebook.com
app_secret = '' # found at developer.facebook.com

# Create fb graph object
fbgraphobj = fb.GraphAPI(access_token)

# Now extend it with the extend_access_token method
extended_token = fbgraphobj.extend_access_token(app_id=app_id, app_secret=app_secret)

print (extended_token)




@app.route("/facebook" , methods=['POST'])
def fbpost():
    if request.method=="POST":
        try:
            getresponse = request.get_json()
            imgBase64 = getresponse['imgstr']
            custID =  getresponse['custID']
            #print(imgBase64)
            
            imgBase64 = str.encode(imgBase64)
            imgDecoded = base64.standard_b64decode(imgBase64)

            imgFile = open("{}.png".format(custID), "wb")
            imgFile.write(imgDecoded)

        
            time.sleep(5)
        
            imgname = str(custID) + ".png"
            print(imgname)
            fbcontent = "Our washer done a great job again" #show our washer done a good job
            fbgraphobj.put_photo(open("" + imgname,"rb"), message =fbcontent)
            return jsonify(
                {
                    "code": 200,
                    "message": "Successfully created Facebook post"
                }
            ), 200
        except Exception as e:
            return jsonify({
                "code":500,
                "message" : "Failed to create a new facebook post"
            }), 500
    



if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5005, debug=True)
