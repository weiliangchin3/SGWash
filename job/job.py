from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
from os import environ

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

customer_complete_URL = environ.get('customer_complete_URL') or "http://localhost:5002/custcompletestatus/"
jobcomplete_URL = environ.get('jobcomplete_URL') or "http://localhost:5001/updatejobcomplete"
facebook_URL = environ.get('facebook_URL') or "http://localhost:5005/facebook"

washercomplete_URL = environ.get('washercomplete_URL') or "http://localhost:5009/washercompletestatus"







@app.route("/processcompleterequest", methods=['PUT'])
def complete_job():
    
    if request.method=="PUT":
        try:
            jobcomplete = request.get_json()
            print('\n-----Starting Job completion Process-----')

            result = processjobcomplete(jobcomplete)  
           
            return jsonify(result), result["code"]

        except Exception as e:
            return jsonify({"code":500 , "message" : "An error occurred in job completion process"})

    
 

def processjobcomplete(jobcomplete):
    try:
        print('\n-----Invoking job request microservice-----')
        jobcomplete_result = invoke_http(jobcomplete_URL + "/" + str(jobcomplete["recordID"]), method='PUT')
        print('jobcomplete_result:', jobcomplete_result)
        custID = jobcomplete['custID']
        washerID = jobcomplete['washerID']
        custdetail = processcuststatus(custID)
        washerdetail = washercompletestatus(washerID) 
        teledetail = telecustcomplete(custdetail)
        fbdetail = facebookpost(jobcomplete) 
        return {
                    "code":200,
                    "message" : "Job has been completed."
                }
    except Exception as e:
            return jsonify({"code":500 , "message" : "An error occurred in job completion process"})
        
  
def processcuststatus(custID):
    print('\n-----Invoking customer booking status microservice-----')
    print()
    customer_complete_result = invoke_http(customer_complete_URL+ str(custID), method='PUT')
    print( customer_complete_result)
    return customer_complete_result
    
def facebookpost(jobcomplete):
    print('\n-----Invoking social media microservice-----')
    
    del jobcomplete['recordID']
    del jobcomplete['washerID']
  
    facebook_result = invoke_http(facebook_URL ,method='POST', json=jobcomplete)
    print('facebook post status:', facebook_result)
    return facebook_result

def washercompletestatus(washerID):
    print('\n-----Invoking washer microservice-----')
    
    washer_complete_result = invoke_http(washercomplete_URL + "/" + str(washerID), method='PUT')
    print('washer_complete_status:', washer_complete_result)
    return washer_complete_result


def telecustcomplete(custdetail):
    print('\n-----Invoking notification microservice-----')

    custteleid= {"telegramID": custdetail['data']['TelegramID']}
    telegram_result = invoke_http("https://notification-gateway-48gyfk5q.de.gateway.dev/customercomplete?key=AIzaSyCfkdAXwQgJcPqgikE6e4sujSb3XbIVFqw" , method='POST', json= custteleid)
    print('telegram_status:', telegram_result)
    return telegram_result

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for updating washer job to completed...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
