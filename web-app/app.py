from flask import Flask, url_for, render_template, redirect
from forms import PredictForm
from flask import request, sessions
import requests
from flask import json
from flask import jsonify
from flask import Request
from flask import Response
import urllib3
import json
# from flask_wtf import FlaskForm

app = Flask(__name__, instance_relative_config=False)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'development key' #you will need a secret key

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')

@app.route('/', methods=('GET', 'POST'))

def startApp():
    form = PredictForm()
    return render_template('index.html', form=form)

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    form = PredictForm()
    if form.submit():

        # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer '
                 + "<eyJraWQiOiIyMDI2MDUxMTA4MjYiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02OTYwMDFNSEE3IiwiaWQiOiJJQk1pZC02OTYwMDFNSEE3IiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMmZlN2IwYjEtNDI3OS00NTZkLWJmNWEtMDEyYjMxZTY5ZmYxIiwiaWRlbnRpZmllciI6IjY5NjAwMU1IQTciLCJnaXZlbl9uYW1lIjoiTXVkYXNlZXIgQWhtZWQiLCJmYW1pbHlfbmFtZSI6Ik1vaGFtbWVkIiwibmFtZSI6Ik11ZGFzZWVyIEFobWVkIE1vaGFtbWVkIiwiZW1haWwiOiJtbW9oYW1tZWQ0QG15Lm5sLmVkdSIsInN1YiI6Im1tb2hhbW1lZDRAbXkubmwuZWR1IiwiYXV0aG4iOnsic3ViIjoibW1vaGFtbWVkNEBteS5ubC5lZHUiLCJpYW1faWQiOiJJQk1pZC02OTYwMDFNSEE3IiwibmFtZSI6Ik11ZGFzZWVyIEFobWVkIE1vaGFtbWVkIiwiZ2l2ZW5fbmFtZSI6Ik11ZGFzZWVyIEFobWVkIiwiZmFtaWx5X25hbWUiOiJNb2hhbW1lZCIsImVtYWlsIjoibW1vaGFtbWVkNEBteS5ubC5lZHUifSwiYXBpa2V5X3V1aWQiOiJBcGlLZXktYjBjOGNjOTgtYTE1Zi00YjdhLWExMGUtMTkwZTk0ZjcyZWM1IiwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiMTM0YWU3NDc0YTE0NDcyY2JkOTk3ZTliZGZmZDJhMGYiLCJpbXNfdXNlcl9pZCI6IjE1NTM3NjcwIiwiZnJvemVuIjp0cnVlLCJpbXMiOiIzMjAyNDg2In0sImlhdCI6MTc4MDgxMTY0NSwiZXhwIjoxNzgwODE1MjQ1LCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.TfRpZNDpt60L7Lr8JxSW_bYfukm3bYgBjGNo-I_PEIj2uvrEBkbz5MLt4O42op2VNgtrvT_tPbMQEcGVXvPHh7yGB04tka34iMZ5rhkqO3WX_vFt-ElfTn6pz8h0pmeGZ_tY9EcA5jByhJc3gKAL4oxwNB5_Q1gZdKTrlJiW09i7bZ3wOWBQ3DBO_A1zn8LHLf77drAsoaFm4-k1uQ33dSm6DN_iulfLkJ6N3ZbBTtPxbaciucetmPujXkGjduvWggen4_bSCnrTISMkL7gfKOs_wCjTcSPT5xQYv1yHx6EVnqyg3zoFyu-TN5XJOmHHtettDeJfdzajng5XfBgM_w
>"}

        if(form.bmi.data == None): 
          python_object = []
        else:
          python_object = [form.age.data, form.sex.data, float(form.bmi.data),
            form.children.data, form.smoker.data, form.region.data]
        #Transform python objects to  Json

        userInput = []
        userInput.append(python_object)

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [{"fields": ["age", "sex", "bmi",
          "children", "smoker", "region"], "values": userInput }]}

        response_scoring = requests.post("https://us-south.ml.cloud.ibm.com/ml/v4/deployments/deploymentinsurance/predictions?version=2021-05-01", json=payload_scoring, headers=header)

        output = json.loads(response_scoring.text)
        print(output)
        for key in output:
          ab = output[key]
        

        for key in ab[0]:
          bc = ab[0][key]
        
        roundedCharge = round(bc[0][0],2)

  
        form.abc = roundedCharge # this returns the response back to the front page
        return render_template('index.html', form=form)
