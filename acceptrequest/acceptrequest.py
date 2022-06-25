from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ
import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

acceptrequest_URL= environ.get('acceptrequest_URL') or "http://localhost:5001/updaterequeststatus/"
washeraccept_URL = environ.get('washeraccept_URL') or "http://localhost:5009/washeracceptstatus/"
cust_accept_status_URL = environ.get('cust_accept_status_URL') or "http://localhost:5002/custacceptstatus/"




@app.route("/processacceptrequest" , methods=['PUT'])
def acceptrequest():
    # Simple check of input format and data of the request are JSON
    if request.method=="PUT":
        print('\n-----Starting job acceptance process-----')
        getacceptrequest = request.get_json()
        print(getacceptrequest)
        try:
            result = processacceptrequest(getacceptrequest)  
            
            return jsonify(result), result["code"]

        except Exception as e:
            return jsonify({"code":500 , "message" : "An error occurred in job acceptance process"})

    # if reached here, not a JSON request.
def processacceptrequest(getacceptrequest):
    try:
        print('\n-----Invoking job request microservice-----')
        acceptrequest = invoke_http(acceptrequest_URL + str(getacceptrequest['recordID']) + "/" + str(getacceptrequest['washerID']), method='PUT')
        print('accept_request status:', acceptrequest)
        print('\n-----Invoking washer microservice-----')
        custID = getacceptrequest['custID']
        
        washerID = getacceptrequest['washerID']
            
        washeraccept = invoke_http(washeraccept_URL + str(washerID), method='PUT')
        washercode = washeraccept["code"]
        print(washeraccept)
                
        print('\n-----Invoking customer microservice-----')
        custaccept = invoke_http(cust_accept_status_URL + str(custID), method='PUT' )
        custcode = custaccept["code"]
        print(custaccept)
        custteleid = (custaccept['data']['TelegramID'])
                
                
        print('\n-----Invoking weather microservice-----')
        weatherurl = "https://weather-api-gateway-48gyfk5q.de.gateway.dev/weather?key=AIzaSyCfkdAXwQgJcPqgikE6e4sujSb3XbIVFqw"
        weatherresponse = invoke_http(weatherurl)
        print(weatherresponse)
        weatherstatus = weatherresponse['data']['status']
                
        print('\n-----Invoking upload image microservice-----')
        url = "https://image-gateway-48gyfk5q.de.gateway.dev/getimgurl?key=AIzaSyCfkdAXwQgJcPqgikE6e4sujSb3XbIVFqw&custID=" + str(custID)
        response = requests.get(url=url)
                    
        print(response.status_code)
        imageresponse = response.json()
                
        print('\n-----Invoking notification microservice-----')
        custteleid = custaccept['data']['TelegramID']
        custteleaccept = {"teleID":custteleid , "weatherStatus":weatherstatus }
        print(custteleaccept)
        #telegram api
        sendcusttele = invoke_http("https://notification-gateway-48gyfk5q.de.gateway.dev/customer?key=AIzaSyCfkdAXwQgJcPqgikE6e4sujSb3XbIVFqw" , method="POST" ,json=custteleaccept)

                

        imageurl = imageresponse['data']['link']
        acceptrequest['data']['imglink'] = imageurl
        return acceptrequest
    except Exception as e:
        return jsonify({"code":500 , "message" : "An error occurred in job acceptance process"})
            
                        
        
           




 

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for updating washer job to completed...")
    app.run(host="0.0.0.0", port=5211, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
