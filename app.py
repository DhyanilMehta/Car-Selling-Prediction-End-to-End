from flask import Flask, render_template, request
from datetime import datetime
# import jsonify
# import requests
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()


@app.route("/predict", methods=['POST'])
def predict():

    if request.method == 'POST':
        num_years = int(request.form['num_years'])
        num_years = datetime.now().year - num_years
        
        present_price = float(request.form['present_price'])
        
        kms_driven = int(request.form['kms_driven'])
        kms_driven_log = np.log(kms_driven)
        
        owner = int(request.form['owner'])
        
        fuel_type_petrol = request.form['fuel_type_petrol']
        if fuel_type_petrol == 'Petrol':
            fuel_type_petrol = 1
            fuel_type_diesel = 0
        
        elif fuel_type_petrol == 'Diesel':
            fuel_type_petrol = 0
            fuel_type_diesel = 1
        
        else:
            fuel_type_petrol = 0
            fuel_type_diesel = 0
        
        seller_type_individual = request.form['seller_type_individual']
        if(seller_type_individual == 'Individual'):
            seller_type_individual = 1
        else:
            seller_type_individual = 0
        
        transmission_manual = request.form['transmission_manual']
        if(transmission_manual == 'Manual'):
            transmission_manual = 1
        else:
            transmission_manual = 0

        prediction = model.predict([[present_price, kms_driven_log, owner, 
                                     num_years, fuel_type_diesel, 
                                     fuel_type_petrol, seller_type_individual, 
                                     transmission_manual]])

        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html',
                                   prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',
                                   prediction_text=f"You can sell the car at {output} Lakhs")
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
