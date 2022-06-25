from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC264ea652db76c46635f8b6aeb319fe4f"
# Your Auth Token from twilio.com/console
auth_token  = "1afca8b8954c57a1ec843ca4fb1bdfb9"

client = Client(account_sid, auth_token)

def sendSMS(otp, mobileNum):
        message = client.messages.create(
        to="+65{}".format(84847957), 
        from_="+12027597499",
        body="Your SGWash OTP is {}".format(otp))
        return None