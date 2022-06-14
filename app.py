from flask import Flask, render_template, request
import pickle
import numpy as np
import sklearn
import matplotlib
from sklearn.preprocessing import StandardScaler
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.sqlite3'  # step 2
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#  database class
db = SQLAlchemy(app) # step 3

# step 4 create a table using python class
class PredHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    tenure = db.Column(db.Integer)
    balance = db.Column(db.Float)
    numOfProducts=db.Column(db.Integer)
    hasCrCard = db.Column(db.Integer)
    isActiveMember = db.Column(db.Integer)
    estimatedSalary = db.Column(db.Float)
    geography_Germany = db.Column(db.String)


    
    # todo write field
    prediction = db.Column(db.Integer)

    def __str__(self):
        return f"{self.id}, {self.prediction}"

### open terminal
### python
### >>> from app import db
### >>> db.create_all()
### >>> exit()

model = pickle.load(open('Customer_Churn_Prediction.pkl', 'rb'))
@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        CreditScore = int(request.form['CreditScore'])
        Age = int(request.form['Age'])
        Tenure = int(request.form['Tenure'])
        Balance = float(request.form['Balance'])
        NumOfProducts = int(request.form['NumOfProducts'])
        HasCrCard = int(request.form['HasCrCard'])
        IsActiveMember = int(request.form['IsActiveMember'])
        EstimatedSalary = float(request.form['EstimatedSalary'])
        Geography_Germany = request.form['Geography_Germany']
        if(Geography_Germany == 'Germany'):
            Geography_Germany = 1
            Geography_Spain= 0
            Geography_France = 0
                
        elif(Geography_Germany == 'Spain'):
            Geography_Germany = 0
            Geography_Spain= 1
            Geography_France = 0
        
        else:
            Geography_Germany = 0
            Geography_Spain= 0
            Geography_France = 1
        Gender_Male = request.form['Gender_Male']
        if(Gender_Male == 'Male'):
            Gender_Male = 1
            Gender_Female = 0
        else:
            Gender_Male = 0
            Gender_Female = 1
        prediction = model.predict([[CreditScore,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Geography_Germany,Geography_Spain,Gender_Male]])
       # record = PredHistory(age=Age, tenure= Tenure,balance=Balance,numOfProducts= NumOfProducts,hasCrCard=HasCrCard,isActiveMember=IsActiveMember, estimatedSalary=EstimatedSalary, geography_Germany=Geography_Germany) # step 6
        # db.session.add(record)
        # db.session.commit()
        if prediction==1:
             return render_template('index.html',prediction_text="Message-The Customer will leave the bank")
        else:
             return render_template('index.html',prediction_text="Message-The Customer will not leave the bank")
                
if __name__=="__main__":
    app.run(debug=True)