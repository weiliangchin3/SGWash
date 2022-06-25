# test_invoke_http.py
from flask import Flask, request, jsonify
import telebot

app = Flask(__name__)

TOKEN = "1553493079:AAF5hdEIFUWRQTZliV2kktls-vgmr6-XhfY"

bot = telebot.TeleBot(TOKEN)

@app.route("/notifywashers", methods=['POST'])
def sendwashernew():
    if request.method == "POST":
        newrequest = request.get_json()
        from_ = -1001200092223
        #print(newrequest["Completetime"])
        reply = '🧽🧴 NEW Job Assignment! 🧽🧴 \n\n Booking type: ' + str(newrequest["bookingType"]) +'\n Carpark Address: ' + str(newrequest["vAddress"]) + '\n Postal Code: ' + str(newrequest["postal"]) + '\n Price: ' +  str(newrequest["cost"]) + '\n Carpark Description: '+ str(newrequest["description"] + '\n Click on the link to login and accept the request http://localhost:5120/login' )
        try:
            bot.send_message(from_,reply)
            return jsonify(
                    {
                        "code": 200,
                        "status": "Successfully notified washers"
                    }
            ), 200
        except Exception as e:
            return jsonify(
                    {
                    "code": 500,
                    "status": "Error sending notification to telegram bot"
                    }
            ), 500


@app.route("/notifycustomer", methods = ["POST"])
def sendcustomernew():
    if request.method == "POST":
        j = request.get_json()
        teleID = int(j['teleID'])
        weatherStatus = j['weatherStatus']
        
        from_ = teleID
            #print(newrequest["Completetime"])
        reply = '🎉 Your car wash request has been accepted by one of our washers! 🎉' 

        if weatherStatus == "delayed":
            reply = "🎉 Your car wash job request has been accepted by one of our washers! However due to inclement weather, our washer might take a little longer to reach to your vehicle. 🎉"
        
        try:
            bot.send_message(from_,reply)
            return jsonify(
                {
                "code": 200,
                "status": "successfully notified customer"
                }
            ), 200
        except Exception as e:
            return jsonify({
                'code' : 500,
                "status" : "Error sending notification to telegram bot"
            }),500

@app.route("/notifycomplete", methods = ["POST"])
def sendcustcomplete():
    if request.method == "POST":
        j = request.get_json()
        teleID = j['telegramID']
        from_ = teleID
            #print(newrequest["Completetime"])
        reply = '✨🚗✨ Our washer has completed cleaning your car! We hope to see you soon! ✨🚗✨' 
        try:
            bot.send_message(from_,reply)
            return jsonify(
                {
                "code": 200,
                "message": "Notification successfully sent to customer"
                }
            ), 200
        except Exception as e:
            return jsonify({
                "code" : 500,
                "status" : "Error sending notification to telegram bot"
            }),500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


