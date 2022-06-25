#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/jobrequest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)
class Jobrequest(db.Model):
    __tablename__ = 'job_request'

    recordID = db.Column(db.Integer, primary_key=True)
    custID = db.Column(db.Integer, nullable=False)
    vAddress = db.Column(db.VARCHAR(255), nullable=False)
    postal = db.Column(db.VARCHAR(255), nullable=False)
    description = db.Column(db.VARCHAR(255), nullable=False)
    bookingType = db.Column(db.VARCHAR(255), nullable=False)
    serviceType = db.Column(db.VARCHAR(255), nullable=False)
    cost = db.Column(db.DECIMAL(asdecimal=False), nullable=False)
    bookDatetime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    washerID = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.VARCHAR(255), nullable=False)
    receiptID = db.Column(db.VARCHAR(255), nullable=False)
   
    carplate = db.Column(db.VARCHAR(255), nullable=False)

   
    def json(self):
        return {'recordID': self.recordID, 'custID': self.custID, 'vAddress': self.vAddress, 'postal': self.postal, 'description': self.description, 'bookingType': self.bookingType, 'serviceType': self.serviceType
        , 'cost': self.cost, 'bookDatetime': self.bookDatetime, 'washerID': self.washerID, 'status': self.status, 'receiptID': self.receiptID,  'carplate': self.carplate  }









@app.route ( "/getalljobrequest" )
def get_all ():
    alljob = Jobrequest.query.filter_by(status="open").all()
    if len(alljob):
        return jsonify(
            {
            "code" : 200 ,
            "data" : {
                "job" : [job.json() for job in alljob]
            }
        }
        )
    return jsonify(
        {
            "code" : 404 ,
            "message" : "There are no jobs."
        }
    ), 404





@app.route ( "/getwasherjob" )
def getwasherjob ():
    washerID = request.get_json()
    print(washerID)
    washerjob = Jobrequest.query.filter_by(status="assigned",washerID=int(washerID)).first()
    if (washerjob):
        return jsonify(
            {
            "code" : 200 ,
            "data" : washerjob.json()
            }
        
        )
    return jsonify(
        {
            "code" : 404 ,
            "message" : "Currently the washer does not have any jobs."
        }
    ), 404




@app.route("/updatejobcomplete/<string:recordID>", methods=['PUT'])
def update_job_status(recordID):
    try:
        
        
        jobcomplete = Jobrequest.query.filter_by(recordID=int(recordID)).first()
        print(jobcomplete)
        if not jobcomplete:
            return jsonify(
                {
                    "code": 404,
                    "message":  "job request not found."
                }
            ), 404

        if jobcomplete:
            jobcomplete.status = "completed"
        
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": jobcomplete.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the job request status. " + str(e)
            }
        ), 500









@app.route("/updaterequeststatus/<string:recordID>/<string:washerID>", methods=['PUT'])
def accept_request(recordID,washerID):
    try:
        acceptrequest = Jobrequest.query.filter_by(recordID=recordID).first()
        
        if not acceptrequest:
            return jsonify(
                {
                    "code": 404,
                    "message": "job request not found."
                }
            ), 404

  
        if acceptrequest.status =="open":
            acceptrequest.status = "assigned"
            print(acceptrequest.json())
            acceptrequest.washerID = washerID
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": acceptrequest.json()
                }
            ), 200
        else:
            return jsonify(
                {
                    "code": 400,
                    "message": "Request has been assigned to other washer"
                }
            ), 400
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the job request status. " + str(e)
            }
        ), 500



if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": to update job request status ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
