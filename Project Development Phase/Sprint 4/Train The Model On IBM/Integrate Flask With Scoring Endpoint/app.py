from flask import render_template,Flask,request,redirect,url_for,g,flash,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import requests
import json

from send_mail import send_email,fail_mail,linear_mail


API_KEY = "Ba1rsbBXQDZJzM50_I8GR6Qon8VzcFbMxEb_jpiJuEGw"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print('mltoken',mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
app.secret_key = '12345'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB']='uaep'

mysql = MySQL(app)
    




# MAIN PAGE
@app.route('/',methods=['GET','POST'])
def main():
    return render_template('index.html')



@app.before_request
def load_user():
    if "username" in session:
        g.record = 1
        g.email = session['email'] 
    else:
        g.record = 0
        
        
#LOGIN page
@app.route('/loginpage',methods = ['GET','POST'])
def loginpage():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from details where username = %s AND password = %s',(username,password))
        account = cursor.fetchone()
        
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            session['email'] = account['email']
            return render_template('prediction.html',username=session['username'],logout='logout')
        else:
        
            return render_template('sign-in.html',msg = 'username and password not found')
    return render_template('sign-in.html')

#logout
@app.route('/logout')
def logout():
    session.pop('username',None)
    return render_template('index.html')

#predict page
@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        toefl = int(request.form.get('toefl'))
        sop = float(request.form.get('sop'))
        lor = float(request.form.get('lor'))
        cgpa = float(request.form.get('cgpa'))
        gre = int(request.form.get('gre'))
        rating = int(request.form.get('rating'))
        researchs = int(request.form.get('researchs'))
        print([toefl,sop,lor,cgpa,gre,rating,researchs])
        model = request.form.get('models')
        if toefl == '':
            msg = 'enter the TOEFL marks'
            return render_template('prediction.html',msg = msg)
        elif sop =='':
            msg = 'enter the SOP marks'
            return render_template('prediction.html',msg = msg)
        elif lor =='':
            msg = 'enter the  LOR marks'
            return render_template('prediction.html',msg = msg)
        elif gre =='':
            msg = 'enter the GRE marks'
            return render_template('prediction.html',msg = msg)
        elif cgpa =='':
            msg = 'enter the CGPA marks'
            return render_template('prediction.html',msg = msg)
        elif researchs =='Select any one':
            msg = 'Please select whether you researched about your admission'
            return render_template('prediction.html',msg = msg)
        elif model =='Select any one':
            msg = 'Please select whether you Naive Bayes Algorithm or Linear Regression Algorithm about your admission'
            return render_template('prediction.html',msg = msg)
                  
            
            
        
           
        if g.record ==1:
            
            value = [[gre,toefl,rating,sop,lor,cgpa,researchs]]
            if model == 'naivebayes':
                payload_scoring = {"input_data": [{"field": [['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research']],
                                    "values": value}]}

                response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5225672f-40af-4161-b95f-ac23c62c8581/predictions?version=2022-11-17', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
                print("Scoring response")
                predictions = response_scoring.json()
                pred = predictions['predictions'][0]['values'][0][0]
                print(pred)
                if pred == 1:
                    send_email(g.email)
                    return render_template('success.html')
                elif pred == 0:
                    fail_mail(g.email)
                    render_template('fail.html')
               
            if model == 'linear':
                payload_scoring = {"input_data": [{"field": [['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research']],
                                    "values": value}]}

                response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/3385d3a8-6854-4b70-bde3-97ddb3152c31/predictions?version=2022-11-17', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
                print("Scoring response")
                predictions = response_scoring.json()
                pred = predictions['predictions'][0]['values'][0][0]
                print(pred)
                return render_template('linear_output.html',prediction= pred)    
                linear_mail(g.email,pred)   
            
        elif g.record == 0:
            # input_lst = [gre,toefl,rating,sop,lor,cgpa,researchs]
            value = [[gre,toefl,rating,sop,lor,cgpa,researchs]]
            
            
            if model == 'naivebayes':
                payload_scoring = {"input_data": [{"field": [['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research']],
                                    "values": value}]}

                response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5225672f-40af-4161-b95f-ac23c62c8581/predictions?version=2022-11-17', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
                print("Scoring response")
                predictions = response_scoring.json()
                pred = predictions['predictions'][0]['values'][0][0]
                print(pred)
                if pred == 1:
                    return render_template('success.html')
                elif pred == 0:
                    render_template('fail.html')
               
            if model == 'linear':
                payload_scoring = {"input_data": [{"field": [['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research']],
                                    "values": value}]}

                response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/3385d3a8-6854-4b70-bde3-97ddb3152c31/predictions?version=2022-11-17', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
                print("Scoring response")
                predictions = response_scoring.json()
                pred = predictions['predictions'][0]['values'][0][0]
                print(pred)
                return render_template('linear_output.html',prediction= pred)    
    if g.record == 1:
        return render_template('prediction.html',username=session['username'],logout = 'logout')
    elif g.record ==0:
        return render_template('prediction.html')
#register page
@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['mail']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM details WHERE username= %s',(username,))
        account = cursor.fetchone()
        
        if account:
            msg = f'{username} already exist please enter an another username'
            return render_template('sign-up.html',msg = msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Enter the valid email id'
            return render_template('sign-up.html',msg = msg)
        elif not re.match( "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", password):
            msg = 'password must be at least 8 character and on special character and one capital letter'
            return render_template('sign-up.html',msg = msg)
        elif password !=confirm_password:
            msg = 'Password and confirm_password must be equal'
            return render_template('sign-up.html',msg = msg)
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
            return render_template('sign-up.html',msg = msg)
        else:
            cursor.execute('Create table if not exists details(username varchar(150),email varchar(150),password varchar(150))')
            cursor.execute('insert into details value(%s,%s,%s)',(username,email,password))
            mysql.connection.commit()
            return render_template('sign-in.html')
    return render_template('sign-up.html')

if __name__ =='__main__':
    app.run(debug=True)