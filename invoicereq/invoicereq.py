#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from flask import Flask, request, jsonify

from invoice import InvoiceGenerator
from sendEmailAPI import sendEmail
import os, sys
import json
import amqp_setup
app = Flask(__name__)


monitorBindingKey='#'



def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'JobRequest'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an invoice request:" + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(order):
    print("Recording an invoice request:")
   
    print(type(order))
    
   
    del order['custID']
    del order['custid']
    del order['bookingType']
    del order['carplate']
    del order['cost']
    del order['description']
    del order['postal']
    del order['vAddress']
    del order['receiptID']
   
    print(order)
    custName = order['custName']
    serviceType = order['serviceType']
    email = order['email']
    invoice = InvoiceGenerator(
    sender="33 Ubi Ave 3, #02-51/52 Vertex, Singapore 408868",
    to=custName,
    logo="https://firebasestorage.googleapis.com/v0/b/fil-flutter-f31f2.appspot.com/o/logo.png?alt=media&token=3976683a-7277-41f8-b409-af4ae175be9d",
    number="",
    notes="Thanks for your business!",
    ship_to="NA",
    )
    invoice.add_item(
    name="Normal Service" if serviceType == "normal" else "Premium Service",
    quantity=1,
    unit_cost="6" if serviceType == "normal" else "9"
    )

      
    pdfname="SGWash-Invoice.pdf"
    invoice.download(pdfname)
    sendEmail(custName, email)


   




if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
