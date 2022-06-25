#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from os import environ
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/washer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class Washer(db.Model):
    __tablename__ = 'washer'

    washerID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(255), nullable=False)
    mobile = db.Column(db.CHAR(255), nullable=False)
    numWashes = db.Column(db.Integer, nullable=False)
    status = db.Column(db.VARCHAR(255), default=False, nullable=False)
 
  

   
    def json(self):
        return {'washerID': self.washerID, 'name': self.name, 'email': self.email, 'password': self.password, 'mobile': self.mobile,  'numWashes': self.numWashes, 'status': self.status}



@app.route("/washerlogin",methods=["POST"])
def washer_login():
    if request.method == "POST":
        j=request.get_json()
        email = j["email"]
        password = j["password"]
        try:
            washerdetails = Washer.query.filter_by(email=email,password=password).first()

            if not washerdetails:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Washer data not found."
                    }
                ), 404
            
            
            return jsonify(
                    {
                        "code": 200,
                        "data": washerdetails.json()
                    }
                ), 200
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while verifying washer account. " + str(e)
                }
            ), 500
    


@app.route("/washeracceptstatus/<string:washerID>", methods=['PUT'])
def update_washeracceptstatus(washerID):
    try:
        washerstatus = Washer.query.filter_by(washerID=washerID).first()
     
        if not washerstatus:
            return jsonify(
                {
                    "code": 404,
                    "message": "Washer data not found."
                }
            ), 404

    
        status = 'unavailable'
        
        if washerstatus.status == "available":
            washerstatus.status = status
            print(washerstatus.json())
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": washerstatus.json()
                }
            ), 200
        else:
            return jsonify({
                "code": 400,
                "message": "Washer only can accept one job"

            })
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the washer status. " + str(e)
            }
        ), 500




@app.route("/washercompletestatus/<string:washerID>", methods=['PUT'])
def update_washercompletestatus(washerID):
    try:
        
        washerstatus = Washer.query.filter_by(washerID=washerID).first()
        
        if not washerstatus:
            return jsonify(
                {
                    "code": 404,
                    "message":  "Washer data not found."
                }
            ), 404

       
        washerstatus.status = "available"
        washerstatus.numWashes = washerstatus.numWashes+1
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": washerstatus.json()
            }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the washer status. " + str(e)
            }
        ), 500







if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": for washer microservice ...")
    app.run(host='0.0.0.0', port=5009, debug=True)
