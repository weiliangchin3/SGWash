import requests
def processRefund(receiptID):
    print('processing refund')
    j = {
            'receiptID' : receiptID,
           
        }
    print(j)
    url = "https://refund-gateway-48gyfk5q.uc.gateway.dev/refund?key=AIzaSyCfkdAXwQgJcPqgikE6e4sujSb3XbIVFqw"
    r = requests.post(url, json= j)
    
    print(r.status_code)
    return r.status_code
    #return 200
def updateTicketDetails(ticketID):
    print('updating ticket')
    url = "http://localhost:5990/updatestatus/" + str(ticketID) 
    
    r = requests.put(url)
    print(r.json()['status'])
    return r.status_code


