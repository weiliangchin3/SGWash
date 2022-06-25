README section
The following microservices listed below are already hosted on Google cloud platform’s cloud run and their respective API gateway HTTP endpoints can be found in the report’s API documentation section. They are not part of the docker-compose setup
1. Image
2. Notification
3. OCR
4. Refund
5. Location verification
6. Weather
Prerequisite to the below setups:
Download the compressed “sgwash” and extract it.


Setup for WAMP
Refer to this link for guide and configuration https://docs.google.com/document/d/1eD8jqLmw9e255NFnPlNVDk_UPhfwt6kOQQ6TspOCMjI/edit
After setup, run the wamp and wait for it to turn green.


Setup for Phpmyadmin Database on localhost
1. Access the PHPmyadmin UI via the link: http://localhost/phpmyadmin/index.php
2. Login into your account with the following details/or your own login details:
User name:root
Password:


3. Click on “User accounts” tab 
4. Make sure you have the root account/settings with no password and “ALL PRIVILEGES”
   1. If needed to change setting, edit “root” privileges and check everything under “Global privileges”


5. Click on “Import”
6. Click “Choose file” 
7. Choose the extracted “G3T7” file and select the “sgwash.sql” file in the "sgwashcode" folder to import with default settings        
Setup for SGWASH User Interface on localhost


1. Open Visual studio Code to run all the UI.
2. Click on file tab and choose “Open Folder”
3. Locate the extracted “G3T7” folder and access the "sgwashcode" folder followed by selecting “SGWASH(UI)” folder, click “Select Folder”
4. Click “Terminal and select “New Terminal
5. In the terminal, install packages required for the UI by entering the following command below:
pip install --no-cache-dir -r requirements.txt
6. In the terminal , type and enter the following command to access the folder.
cd scenario 1        
7. Type and enter the following command to run the UI for scenario 1.
python app.py 
8. Click the “+” sign on the upper right of the terminal to create a new terminal and Repeat the same step 7-8 for scenario 2, 3 and 4 to run the remaining UI.


9. Check if the UI is accessible via the below URL for each scenario:
   1. Scenario 1 Customer SignUp URL : http://localhost:5700/signup


   2. Scenario 2 Customer Create new Job Request URL : http://localhost:5111/login


   3. Scenario 3 & 4 Washer Accept and Complete Job Request URL : http://localhost:5120/login
   4. Scenario 5 Customer refund ticket : http://localhost:5440/tickets






Setup for docker-compose


1. Open Visual Studio Code 
2. Click on file tab and choose “Open Folder”
3. Locate your extracted “G3T7” folder followed by "sgwashcode" folder and select that folder
4. Click on “docker-compose.yml” file under “explorer”
 
5. In the “ docker-compose.yml” file, there is this code for each microservices:
image: wpchen2019/<microservice_name>:esd


Change the “wpchen2019” to your own dockerID. Do the same changes
for all the microservices  except for “rabbitmq” messaging broker. Save it after done.
6. Click “Terminal and select “New Terminal
7. Make sure you are in the same directory as the docker compose yml file and run the following docker compose command:
docker-compose up --force-recreate


8. Will take some time to build and wait until it turn green in the docker application 


9. Our solution is good to use now.
        Gmail account for your testing on invoice and gmail api:
        Gmail: esdprojectg7@gmail.com
        Password: !123qweASD
   1. Scenario 1 Customer SignUp URL(Only Signup function): http://localhost:5700/signup
      1. For the twilio verification, the terminal will print out the 6 digit OTP due to the limitation of a free account

   #when you are prompt to upload your car photo after registration, use the car photo "customersignup.png" in the following directory sgwashcode/SGWASH(UI)/car

   2. Scenario 2 Customer Create new Job Request URL(Only Job creation function) : http://localhost:5111/login


   3. Scenario 3 & 4 Washer Accept and Complete Job Request URL(Only Washer acceptance and completion of job) : http://localhost:5120/login


         Washer email: john@gmail.com
         Password:123
           Or 
         Washer email: may@gmail.com
         Password:345
#For the OCR function after the image is submitted upon job request, use the car photo "washercomplete.png" in the following directory sgwashcode/SGWASH(UI)/car.
To simulate the real situation of a washer finishing his job, the OCR scan result will be shown on the terminal

   4. Link to SGWASH facebook page to verify the facebook api works after job completion
          https://www.facebook.com/Sgwash_esd-103223595186864
   5. Scenario 5 Customer refund ticket : http://localhost:5440/tickets