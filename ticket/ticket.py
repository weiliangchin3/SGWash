from flask import Flask, jsonify,request
import mysql.connector

app = Flask(__name__)

def convertData(data):
    output = []
    for row in data:
        json = {
            'tixID' : row[0],
            'custID' : row[1],
            'recordID' : row[2],
            'date_submit' : row[3],
            'time_submit' : row[4],
            'receiptID' : row[5],
            'description' : row[6],
            'status' : row[7],
            'image_URL' : row[8],
            'amount' : row[9]
        }
        output.append(json)
    return output
# GET all tickets where status is "open"
@app.route("/tickets")
def index():
    connection = mysql.connector.connect(
        host="host.docker.internal",
        user='root',
        password='',
        database='ticket'
        
        
    )
    query = "SELECT * FROM ticket WHERE status = 'open'"
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall() # type is array
        connection.close()
        result = convertData(result)
        #print(result)
        return jsonify({
            'code' : 200,
            'data' : {
                "tickets" : result
            }
        })
    except Exception as e:
        print(e)
        return jsonify({
            'code' : 500,
            'status' : 'Error connecting to DB'
        }),500

# Get ticket by ID
# @app.route('/ticketID')
# def getTicket():
#     connection = mysql.connector.connect(
#         host="35.192.149.80",
#         user='root',
#         password='root',
#         database='sgwash',
#     )
#     ticketID = request.args.get('ticketID')
#     query = "SELECT * FROM ticket WHERE tixID = '{}'".format(ticketID)
#     cursor = connection.cursor()
#     cursor.execute(query)
#     result = cursor.fetchall() # type is array
#     print(len(result))
#     if len(result) != 0:
#         result = convertData(result)
#         connection.close()
#         return jsonify({
#             'code' : 200,
#             'data' : {
#                 "ticket" : result[0]
#             }
#         })
#     return jsonify({
#         'code' : 200,
#         'status' : 'Ticket ID {} not found in database'.format(ticketID)
#     }),200

# Update ticket status to "closed"
@app.route('/updatestatus/<string:ticketID>', methods=['PUT'])
def updateTicket(ticketID):
    print(ticketID)
    connection = mysql.connector.connect(
        host="host.docker.internal",
        user='root',
        password='',
        database='ticket',
    )
    query = "UPDATE ticket SET status = 'closed' WHERE tixID = '{}'".format(ticketID)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()
    if cursor.rowcount == 1:
        return jsonify({
            'code' : 200,
            'status' : 'Ticket status sucessfully changed'
        }),200
    return jsonify({
        'code' : 404,
        'status' : 'Ticket not found'
    }),404

if __name__ == "__main__":
    app.run(debug=True, port=5990, host="0.0.0.0")