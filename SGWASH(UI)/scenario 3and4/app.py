from flask import Flask,jsonify, render_template, request, redirect, session, url_for
from functions import *
import base64

app = Flask(__name__)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print('hi')
        emailInput = request.form['email']
        passInput = request.form['password']
        #invoke washer microservice
        url = "http://localhost:5009/washerlogin"
        print(url)
        washerlogindetail= {"email":emailInput , "password": passInput}
        response = requests.post(url,json=washerlogindetail)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            
            session['accInfo'] = {
                "washerID" : data['data']['washerID'],
                "name" : data['data']['name'],
                "mobile" : data['data']['mobile'],
                "email" : data['data']['email'],
                "password" : data['data']['password'],
                "numWashes" : data['data']['numWashes'],
             
                "status" : data['data']['status']
            }
            return redirect(url_for('jobs'))
    return render_template('login.html')

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    washerInfo = session['accInfo']
    washerID = washerInfo['washerID']
    washerStatus = washerInfo['status']
    print('washer status is {}'.format(washerStatus))
    
    # microservice to get all jobs
    
    
    if washerStatus == "unavailable":
        
        print(washerID)
        #invoke job request microservice
        url= "http://localhost:5001/getwasherjob"
       
        response = requests.get(url=url,json=washerID)
        washerjob = response.json()
       
        session['job']=washerjob['data']
        return redirect(url_for('job'))
    jobs = getJobs()
    if jobs['code']== 200:
        jobs = jobs['data']['job']
    else:
        return render_template('nojobs.html')
    custID = (jobs[0]['custID'])
    if request.method == "POST":
        
        recordID = request.form['recordID']
        
        acceptrequest = {"recordID":recordID,"washerID":washerID,"custID":custID}
        print(acceptrequest)
        #invoke accept orchestrator
        url = "http://localhost:5211/processacceptrequest"
        response = requests.put(url=url,json=acceptrequest)
        print("this the result:",response.json())
        
        if response.status_code ==200:
            jobresponse = response.json()
            imglink = jobresponse['data']['imglink']
            jobdetails = jobresponse['data']
            
            session['job']=jobdetails
            session['imglink'] = imglink
            return redirect(url_for('job'))
        print(session['accInfo'])
        return redirect(url_for('job'))
        return render_template('job.html')
    
    return render_template('jobs.html',  jobs = jobs)

@app.route('/job', methods=['POST', 'GET'])
def job():
    jobDetails = session['job']
    imglink = session['imglink']
    if request.method == "POST":
        if request.files['img'].filename == "":
            print('file name is empty')
        else:
            imageUploaded = request.files['img']
            print(imageUploaded.filename)
            img_string = base64.b64encode(imageUploaded.read())
        
            img_string = img_string.decode('ascii')
            img_object = {"base64" : img_string}
            #invoke OCR MICROSERVICE
            ocrcheck = requests.post(url="https://ocr-gateway-48gyfk5q.de.gateway.dev/ocr?key=AIzaSyCfkdAXwQgJcPqgikE6e4sujSb3XbIVFqw",json=img_object)
           
            if ocrcheck.status_code == 200:
                data = ocrcheck.json()
                carplateocr = data['data']['pNum']
               
                print(data)
                
                print(jobDetails['carplate'])
                
                numbers = sum(c.isdigit() for c in carplateocr)
                print(numbers)

                #improving the accuracy of OCR 
                if numbers == 3 :
                    if "-" not in carplateocr[0:4]:
                        carplateocr = carplateocr[0:3] + "-" + carplateocr[3:len(carplateocr)]

                    if "-" not in carplateocr[5:len(carplateocr)]:
                                carplateocr =  carplateocr[0:7] + "-" + carplateocr[7]

                
                else:
                    if "-" not in carplateocr[0:4]:
                        carplateocr = carplateocr[0:3] + "-" + carplateocr[3:len(carplateocr)]

                    if "-" not in carplateocr[5:len(carplateocr)]:
                                carplateocr =  carplateocr[0:8] + "-" + carplateocr[8:len(carplateocr)]
                print("OCR Scan Result:" + carplateocr)
                
                #CHECK if ocr ressult same as user input car plate number
                if jobDetails['carplate'] == carplateocr:

                    
                    jobcompletedetail = {"imgstr":img_string,
                                         "recordID": jobDetails['recordID'],
                                         "custID": jobDetails['custID'],
                                         "washerID": jobDetails['washerID']}
                    #invoke job orchestrator
                    url = "http://localhost:5100/processcompleterequest"
                    response = requests.put(url=url,json=jobcompletedetail)
                
                    if response.status_code ==200:
                        jobcomplete = response.json()
                        print (jobcomplete)
                    return render_template('success.html')
                else:
                    return render_template('fail.html')

        
    return render_template('job.html', job = jobDetails, imglink = imglink)

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run(debug=True, port=5120, host="0.0.0.0")