from flask import Flask, render_template, request
# used to run/serve our application
# render_template is used for rendering the html pages
#import load from joblib to load the saved model file
from joblib import load

app=Flask(__name__) # our flask app
#load model file
import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "AaKFzAr-QMG9qaaO4eQpB9IzmeNL9etl2OCko8uXQB2t"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

model =load('floods.save')
sc=load('transform.save')


@app.route('/') # rendering the html template
def home():
    return render_template('home.html')
@app.route('/predict') # rendering the html template
def index() :       
    return render_template("index.html")


@app.route('/data_predict', methods=['POST']) # route for our prediction
def predict():
    temp = request.form['temp']
    Hum = request.form['Hum']
    db = request.form['db']
    ap = request.form['ap']
    aa1 = request.form['aa1']

    data = [[float(temp),float(Hum),float(db),float(ap),float(aa1)]]
    
    payload_scoring = {"input_data": [{"field": ["Cloud Cover","ANNUAL","Jan-Feb","Mar-May","Jun-Sep"], "values": data}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/bb6d4e4b-0344-4813-9296-8fbedcc685bd/predictions?version=2022-08-09', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("response_scoring")
    prediction=response_scoring.json()
    output=prediction["predictions"][0]["values"][0][0]
    if(output==0):
        return render_template('noChance.html', prediction='No possibility of severe flood')
    else:
        return render_template('chance.html', prediction='possibility of severe flood')

if __name__ == '__main__':
    app.run(debug=False)