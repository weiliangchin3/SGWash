from flask import Flask, jsonify
import requests

apiKey = '37fb27f535f41e235acd80ab982f43e8'

app = Flask(__name__)
@app.route('/weatherstatus')
def getWeather():
    url = "https://api.openweathermap.org/data/2.5/weather?q=Singapore&appid={}".format(apiKey)
    badConditions = ['Thunderstorm', 'Drizzle', 'Rain']
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        status = ''
        condition = data['weather'][0]['main']
        # Bad weather types
        # Thunderstorm
        # Drizzle
        # Rain
        if condition in badConditions:
            status = 'delayed'
        else:
            status = 'normal'
        return jsonify({
            'code' : 200,
            "data" : {
                'condition' : condition,
                'status' : status 
            },
            
        }),200
    return jsonify({
        'code' : 500,
        'status' : 'Unable to get weather data from API'
    }),500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000 )


    