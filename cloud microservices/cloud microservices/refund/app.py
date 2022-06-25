from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51ICm2CImR2bGEHhXPctWYJfYRCzdP5tvRWkmXLtR1ZvMHsd3MZobArFYxuzNd7cBstDaOLkHLYGD3FMU76pjDrFF00IZBjrgXd'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51ICm2CImR2bGEHhX52zTUENa7RvNRToWSVJjlCmpqUcucLNWpasjdYi6W2CuEVnUsXZNt2clzXpxog9itDrPJ4RJ00lYVJ07dr'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route('/refund', methods=['POST', 'GET'])
def index():
    status = ''
    if request.is_json:
        inputJson = request.get_json()
        chargeID = inputJson['receiptID']
        try:
            stripe.Refund.create(
                charge = chargeID
            )
            status = "Refund successful"
            return jsonify({
                'code' : 200,
                'status' : status
            }),200
        except Exception as e:
            print(e)
            status = "Charge is already refunded"
            return jsonify({
                'code' : 400,
                'status' : status
            }),400
    return jsonify({
        'code' : 500,
        'status' : 'refund was not successful'
    }),500
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)