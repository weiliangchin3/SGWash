from flask import Flask, render_template,url_for, request, session, jsonify, redirect
import requests,secrets, time
import send_sms
import base64


app = Flask(__name__)



def generateVerification():
    randomNumber = ""
    for _ in range(6):
        num = str(secrets.randbelow(9))
        randomNumber += num
    randomNumber = int(randomNumber)
    return randomNumber

@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    errors = []
    if request.method == "POST":
        name = request.form['name']
        mobileNum = request.form['number']
        email = request.form['email']
        teleID = request.form['teleID']
        password = request.form['pass']
        vType = request.form['vType']
        cPlate = request.form['cPlate']
        if len(mobileNum) != 8:
            errors.append('Phone number is invalid')
            return render_template('signup.html', errors = errors)
        userInfo = {
            'name' : name,
            'mobileNum' : mobileNum,
            'email' : email,
            'teleID' : teleID,
            'password' : password,
            'vType' : vType,
            'cPlate' : cPlate
        }
        # invoke microservice to check if account exist
        url = "http://localhost:5002/mobile?mobile={}".format(mobileNum)
        r = requests.get(url)
        if r.status_code != 200:
            print(r.status_code)
            randomNumber = generateVerification()
            session['userInfo'] = userInfo
            session['randomNum'] = randomNumber
            session['runonce']= False
            return redirect(url_for('verification'))
        else:
            errors.append("Account already exist")
    return render_template('signup.html', errors = errors)

@app.route('/verification', methods = ['GET', 'POST'])
def verification():
    userInfo = session['userInfo']
    mobileNum = session['userInfo']['mobileNum']
    error = ""
    resend = ""
    randomNumber = session['randomNum']
    print(randomNumber)
    if not session['runonce']:
        print('OTP is {}'.format(randomNumber))
        # invoke twilio API
        send_sms.sendSMS(randomNumber,mobileNum)
        session['runonce']=True

    if request.method == "POST":
        verInput = request.form['verification']
        print('input number is {}'.format(verInput))

        
        if int(verInput) == randomNumber:
            print('match')
            url = "http://localhost:5002/createcustomer"
            j = {
                "name" : userInfo['name'],
                "mobile":userInfo['mobileNum'],
                "email":userInfo['email'],
                "password":userInfo['password'],
                "vType":userInfo['vType'],
                "verified":"0",
                "carplate":userInfo['cPlate'],
                "bookingStatus":"available",
                "telegramID":userInfo['teleID']
            }
            createresponse = requests.post(url=url, json=j)
            print(createresponse.json())
            # when user verification input match post to customer microservice to add user details to DB
            # change below accordingly, add the route name after the slash

            #requests.post('http://localhost:5000/', json = session['userInfo']) # assuming ur container is mapped to 5000

            # after POST to DB, check if DB created new entry by doing a GET request and store the custID
            # url = "" # url to microservice - retrieve user info by phone number
            time.sleep(5) # 5 second delay
            url = "http://localhost:5002/mobile?mobile={}".format(userInfo['mobileNum'])
            query = requests.get(url)
            data = query.json()
            custID = data['data']['custID']
            print(custID)

            # pass the custID in the URL
            
            # return redirect(url_for('upload'))
            return redirect(url_for('upload', custID = custID))

        else:
            error = "Verification code is invalid."
            print('not match')
    
    
    return render_template('verification.html', number = mobileNum, error = error, resend = resend )

@app.route('/upload/<custID>', methods = ["POST", "GET"])
def upload(custID):
    if request.method == "POST":
        if request.form['type'] == 'upload':
            print(request.form['type'])
            if request.files['img'].filename == "":
                print('file name is empty')
            else:
                imageUploaded = request.files['img']
                img_string = base64.b64encode(imageUploaded.read())
            
                img_string = img_string.decode('ascii')
                #print("base64 is {}".format(img_string))
                # POST request to image upload microservice
                url = "https://image-gateway-48gyfk5q.de.gateway.dev/uploadimg?key=AIzaSyCfkdAXwQgJcPqgikE6e4sujSb3XbIVFqw"
                # get custID from session
                j = {
                    'folderName' : "userVehicles",
                    'custID' : str(custID),
                    'base64': img_string,
                }
                requests.post(url=url, json=j)
                session.clear()
                return render_template('imageSuccess.html')
                
        else:
            return redirect(url_for('main'))
    return render_template('upload.html')





if __name__ == "__main__":
    app.secret_key = 'key'
    app.run(host="0.0.0.0", port=5700, debug=True)



