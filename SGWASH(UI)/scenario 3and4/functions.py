
import requests


def getJobs():
    url = "http://localhost:5001/getalljobrequest"
    response = requests.get(url)
    getresponse = (response.json())
    return getresponse
    


