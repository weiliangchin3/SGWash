from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ
import requests
from invokes import invoke_http
import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

createcuststatus_URL = environ.get('createcuststatus_URL') or  "http://localhost:5002/updatecuststatus"


@app.route("/newrequest", methods=['PUT'])
def newrequest():
  
    if request.is_json:
        try:
            print('\n-----Starting Job creation process-----')
            newrequest = request.get_json()
            

          
            result = updatecuststatus(newrequest)  
           
            return jsonify(result), result["code"]

        except Exception as e:
            return jsonify({"code":500 , "message" : "An error occurred in job creation process"}) 

def updatecuststatus(newrequest):
    try:
        print('\n-----Invoking customer microservice-----')
        custID = newrequest["custID"]
        checkcust = invoke_http(createcuststatus_URL + "/" + str(custID), method='PUT')
        print('cust_booking status:', checkcust)
    
    
        custname = checkcust['data']['name']
        custemail = checkcust['data']['email']
        custid = checkcust['data']['custID']
        servicetype = newrequest['serviceType']
        custinvoice = {"custName":custname,"serviceType":servicetype,"email":custemail,"custid":custid}
        print(custinvoice)
        combineinfo = {**newrequest, **custinvoice}

            #invoke job request to create request
        newrequestresult = processnewquest(combineinfo)

            #invoke invoice to generate invoice
            #invoiceresult = processinvoice(combineinfo)

            #invoke telegram to notify washer
        print('\n-----Invoking notification microservice-----')
        tele_notification_status = invoke_http("https://notification-gateway-48gyfk5q.de.gateway.dev/washers?key=AIzaSyCfkdAXwQgJcPqgikE6e4sujSb3XbIVFqw", method='POST', json=newrequest)
        print( "telegram status:" ,tele_notification_status)
        
        return {
                "code":200,
                "message" : "Tele notification has been sent"
            }
    except Exception as e:
        return jsonify({"code":500 , "message" : "An error occurred in job creation process"})

def processnewquest(combineinfo):
    
    message = json.dumps(combineinfo)
    print("amqp new job request")
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key='#', 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key='#', 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))
    print("\Request(new job) published to RabbitMQ Exchange.\n")

# def processinvoice(combineinfo):
#     message = json.dumps(combineinfo)
#     print("amqp invoice generate")
#     amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key='JobRequest', 
#             body=message, properties=pika.BasicProperties(delivery_mode = 2))
#     print("\Request(invoice) published to RabbitMQ Exchange.\n")


 

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for updating washer job to completed...")
    app.run(host="0.0.0.0", port=5200, debug=True)
    