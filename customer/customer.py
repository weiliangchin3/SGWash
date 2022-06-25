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
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/customer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)

class Cust(db.Model):
    __tablename__ = 'customer'

    custID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False)
    mobile = db.Column(db.CHAR(255), nullable=False)
    email = db.Column(db.VARCHAR(255), nullable=False)
    password = db.Column(db.VARCHAR(255), nullable=False)
    vType = db.Column(db.VARCHAR(255), nullable=False)
    carplate = db.Column(db.VARCHAR(255), nullable=False)
    verified = db.Column(db.VARCHAR(1), default=False, nullable=False)
    bookingStatus = db.Column(db.VARCHAR(1), default=False, nullable=False)
    TelegramID = db.Column(db.VARCHAR(255), nullable=False)
  
    def __init__(self, name, mobile, email, password, vType, carplate, verified, bookingStatus, TelegramID):
        self.name = name
        self.mobile = mobile
        self.email = email
        self.password = password
        self.vType = vType
        self.carplate = carplate
        self.verified = verified
        self.bookingStatus = bookingStatus
        self.TelegramID = TelegramID
   
    def json(self):
        return {'custID': self.custID, 'name': self.name, 'mobile': self.mobile, 'email': self.email, 'password': self.password, 'vType': self.vType, 'carplate': self.carplate
        , 'verified': self.verified, 'bookingStatus': self.bookingStatus, 'TelegramID': self.TelegramID}



@app.route("/createcustomer", methods=['POST'])
def create_customer():
    if request.is_json:
        inputJSON = request.get_json()
        print(inputJSON)
        name = inputJSON['name']
        mobile = inputJSON['mobile']
        email = inputJSON['email']
        password = inputJSON['password']
        vType = inputJSON['vType']
        carplate = inputJSON['carplate']
        verified = "1"
        bookingStatus = "Available"
        TelegramID = inputJSON['telegramID']
  

    customer = Cust(name,mobile,email,password,vType,carplate,verified,bookingStatus,TelegramID)
    

    try:
        db.session.add(customer)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 404,
                "message": "An error occurred creating the customer."
            }
        ), 404

    return jsonify(
        {
            "code": 201,
            "data": customer.json()
        }
    ), 201



@app.route("/mobile")
def find_by_custID():
    mobile = request.args.get('mobile')
    print(mobile)
    customer = Cust.query.filter_by(mobile=mobile).first()
    if customer:
        return jsonify(
            {
                "code": 200,
                "data": customer.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Customer not found."
        }
    ), 404





@app.route("/custlogin",methods=["POST"])
def cust_login():
    if request.method == "POST":
        j=request.get_json()
        email = j["email"]
        password = j["password"]
        try:
            custdetails = Cust.query.filter_by(email=email,password=password).first()

            if not custdetails:
                return jsonify(
                    {
                        "code": 404,
                        "message": "Customer data not found."
                    }
                ), 404

            return jsonify(
                    {
                        "code": 200,
                        "data": custdetails.json()
                    }
                ), 200
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while verifying customer account. " + str(e)
                }
            ), 500




@app.route("/getcustbookingstatus",)
def cust_status():
    custID = request.args.get("custID")
    
    try:
        custdetails = Cust.query.filter_by(custID=custID).first()

        if not custdetails:
            return jsonify(
                {
                    "code": 404,
                    "message": "Customer data not found."
                }
            ), 404

      
        custinfo = custdetails.json()
        custbooking = custinfo['bookingStatus']
        return jsonify(
                {   "code":200,
                    "data": {"bookingStatus": custbooking
                            }
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while retrieving customer status. " + str(e)
            }
        ), 500




@app.route("/custcompletestatus/<string:custID>", methods=['PUT'])
def update_customerstatus(custID):
    try:
        custbookingstatus = Cust.query.filter_by(custID=custID).first()
     
        if not custbookingstatus:
            return jsonify(
                {
                    "code": 404,
                    "message": "Customer data not found."
                }
            ), 404

       
        
        if custbookingstatus:
            custbookingstatus.bookingStatus = 'Available'
           
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": custbookingstatus.json()
                }
            ), 200
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message":  "An error occurred while updating the customer status. " + str(e)
            }
        ), 500




@app.route("/custacceptstatus/<string:custID>", methods=['PUT'])
def cust_accept_status(custID):
    try:
        custacceptstatus = Cust.query.filter_by(custID=custID).first()
     
        if not custacceptstatus:
            return jsonify(
                {
                    "code": 404,
                    "message": "Customer data not found."
                }
            ), 404

        
        status = "booked"
        cust_status = custacceptstatus.bookingStatus
        print(cust_status)
        if cust_status == "pending" :
            custacceptstatus.bookingStatus = status
           
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": custacceptstatus.json()
                }
            ), 200
        else:
            return jsonify(
                {
                    "code": 400,
                    "message": "Customer request has been taken"
                }


            )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the customer status. " + str(e)
            }
        ), 500



@app.route("/updatecuststatus/<string:custID>", methods=['PUT'])
def cust_create_status(custID):
    try:
        custcreatestatus = Cust.query.filter_by(custID=custID).first()
        
        if not custcreatestatus:
            return jsonify(
                {
                    "code": 404,
                    "message": "Customer data not found."
                }
            ), 404

            # update status #json to python
        status = "pending"
        cust_status = custcreatestatus.bookingStatus
           
        if cust_status == "Available" :
            custcreatestatus.bookingStatus = status
               
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": custcreatestatus.json()
                }
            ), 200
        else:
            return jsonify(
                {
                    "code": 400,
                    "message": "Customer has already made a request"
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while updating the customer status. " + str(e)
            }
        ), 500



if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": for customer microservice ...")
    app.run(host='0.0.0.0', port=5002, debug=True)
