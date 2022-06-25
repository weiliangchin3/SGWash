from flask import Flask, render_template,url_for, request, session, jsonify, redirect
from flask_cors import CORS
import requests,secrets, time

import base64
import stripe

app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51ICm2CImR2bGEHhXPctWYJfYRCzdP5tvRWkmXLtR1ZvMHsd3MZobArFYxuzNd7cBstDaOLkHLYGD3FMU76pjDrFF00IZBjrgXd'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51ICm2CImR2bGEHhX52zTUENa7RvNRToWSVJjlCmpqUcucLNWpasjdYi6W2CuEVnUsXZNt2clzXpxog9itDrPJ4RJ00lYVJ07dr'

stripe.api_key = app.config['STRIPE_SECRET_KEY']
CORS(app)
normalPrice = "price_1ISOiaImR2bGEHhXsyWS2s2O"
premiumPrice = "price_1ISOjCImR2bGEHhXNaFCA0NS"



@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/booking', methods=['POST', 'GET'])
def index():
    bookingStatus = session['accInfo']['bookingStatus']
    custID = session['accInfo']['custID']
    #invoke customer microservice to check if their status is 'available'
    bookstatusurl = "http://localhost:5002/getcustbookingstatus?custID={}".format(custID)
    bookresponse = requests.get(url=bookstatusurl)
    bookstatus = bookresponse.json()
    bookingStatus = bookstatus["data"]["bookingStatus"]
    print(bookingStatus)
    
    if bookingStatus == "Available":
        userInfo = session['accInfo']
        pCode = userInfo['carplate']
        custID = userInfo['custID']
        teleID = userInfo['telegramID']
        
        return render_template('booking.html', pCode = pCode, teleID = teleID, custID = custID)
    else:
        return render_template('noBooking.html')

@app.route('/payment',methods=['POST', 'GET'])
def payment():
    
    bookingdetail = request.get_json()
   
    item = {
        "price" : normalPrice if bookingdetail['serviceType'] == "normal" else premiumPrice,
        "quantity" : 1
    }
  
    if item['price'] == "price_1ISOiaImR2bGEHhXsyWS2s2O":
        cost = 6
    else:
        cost = 9
    
    bookingdetail['cost']=cost
   
    session['bookingdetail']=bookingdetail
    checkout_session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items=[item],
        mode = 'payment',
        success_url = url_for("success", _external=True),
        cancel_url = url_for('cancel', _external = True ),
    )
    session['payment_intent'] = checkout_session['payment_intent']
    
    return{
        'checkout_session_id' : checkout_session['id'],
        'checkout_public_key' : app.config['STRIPE_PUBLIC_KEY']
    }

@app.route('/success')
def success():
    bookingdetail = session['bookingdetail']
    
    custID = session['accInfo']['custID']
    teleID = session['accInfo']['telegramID']
    bookingdetail['custID']=custID
   
    # this route will pass the booking details to the request microservice 
    # pass all required data to request (orchestrator)
    paymentIntent = session['payment_intent']
    r = stripe.PaymentIntent.retrieve(
        paymentIntent
    )
    receiptID = r['charges']['data'][0]['id']
    bookingdetail['receiptID']=receiptID
    print(bookingdetail)
    #invoke request orchestrator
    url = "http://localhost:5200/newrequest"
    response = requests.put(url=url, json = bookingdetail)
    print(response.json())
    if response.status_code:
        return render_template('success.html')
    print(session['accInfo'])
    return jsonify({
        'paymentIntent' : paymentIntent,
        'chargeID' : receiptID,
        'teleID' : teleID,
        'custID' : custID
    }),200
   

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        
        email = request.form['email']
        password = request.form['password']
        #invoke customer microservice
        url = "http://localhost:5002/custlogin"
        custlogindetail= {"email":email , "password": password}
        print(url)
        response = requests.post(url, json=custlogindetail)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            
            session['accInfo'] = {
                "custID" : data['data']['custID'],
                "name" : data['data']['name'],
                "mobile" : data['data']['mobile'],
                "email" : data['data']['email'],
                "password" : data['data']['password'],
                "vType" : data['data']['vType'],
                "carplate" : data['data']['carplate'],
                "verified" : data['data']['verified'],
                "bookingStatus" : data['data']['bookingStatus'],
                "telegramID" : data['data']['TelegramID']
            }
            return redirect(url_for('main'))
    return render_template('login.html')

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run(host="0.0.0.0", port=5111, debug=True)



