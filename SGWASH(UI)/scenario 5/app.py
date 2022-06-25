from flask import Flask, render_template, redirect, url_for, request, session
from functions import *

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('tickets'))

@app.route('/tickets', methods = ['POST', 'GET'])
def tickets():
    url = "http://localhost:5990/tickets"
    response = requests.get(url)
    
    tickets = response.json()['data']['tickets']
    #print(tickets["tickets"])
    if request.method == "POST":
        session['ticket'] = {
            'tixID' : request.form['ticketID'],
            'custID' : request.form['custID'],
            'recordID' : request.form['recordID'],
            'dateSubmit' : request.form['dateSubmit'],
            'timeSubmit' : request.form['timeSubmit'],
            'receiptID' : request.form['receiptID'],
            'description' : request.form['description'],
            'imageURL' : request.form['imageURL'],
            "amount" : request.form['amount']
        }
        return redirect(url_for('ticketDetails'))
    
    return render_template('tickets.html', tickets = tickets)

@app.route('/details', methods=['GET', 'POST'])
def ticketDetails():
    # url = "https://ticket-7w5grnntvq-uc.a.run.app/ticketID?ticketID={}".format(ticketID)
    # response = requests.get(url)
    # ticket = response.json()['data'][0]
    ticket = session['ticket']
    ticketID = ticket['tixID']
    print(ticket)
    if request.method == "POST":
        receiptID = ticket['receiptID']
        statusCode = processRefund(receiptID)
        if statusCode == 200:
            statusCode = updateTicketDetails(ticketID) 
            return redirect(url_for('refunded'))
    return render_template('ticketDetails.html', ticket = ticket)

@app.route('/refunded', methods = ['POST', 'GET'])
def refunded():
    if request.method == 'POST':
        return redirect(url_for('tickets'))
    return render_template('refunded.html')

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run(debug=True, port=5440, host="0.0.0.0")