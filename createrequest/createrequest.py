#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from flask import Flask, request, jsonify
from datetime import datetime
import requests
from invokes import invoke_http
from flask_cors import CORS
import os, sys
from os import environ
from flask_sqlalchemy import SQLAlchemy
import json
import amqp_setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/jobrequest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)
monitorBindingKey='#'
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
    
    washerID = db.Column(db.Integer, nullable=True)
    status = db.Column(db.VARCHAR(255), nullable=False, default="open")
    receiptID = db.Column(db.VARCHAR(255), nullable=False)
    
    carplate = db.Column(db.VARCHAR(255), nullable=False)
    

   
    def json(self):
        return {'recordID': self.recordID, 'custID': self.custID, 'vAddress': self.vAddress, 'postal': self.postal, 'description': self.description, 'bookingType': self.bookingType, 'serviceType': self.serviceType
        , 'cost': self.cost, 'bookDatetime': self.bookDatetime, 'washerID': self.washerID, 'status': self.status, 'receiptID': self.receiptID, 'carplate': self.carplate  }



def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'JobRequest'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an new job request:" + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(order):
    print("Recording an new job request:")

    print(type(order))
  
    del order['custName']
    
    del order['email']
    del order['custid']
   
    print(order)
    newrequest = Jobrequest(**order)
  
    try:
        db.session.add(newrequest)
        db.session.commit()
        print("AMQP status:", "successfully created a new request")
        
    except:
        print('AMQP status:', "failed to create request")

   




if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
