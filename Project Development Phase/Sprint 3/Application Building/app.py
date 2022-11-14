from flask import render_template,Flask,request,redirect,url_for,g,flash,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import numpy as np
import pandas as pd
import joblib

from send_mail import send_email,fail_mail,linear_mail

app = Flask(__name__)
app.secret_key = '12345'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB']='uaep'

mysql = MySQL(app)
    

"""Prediction code"""  
scaler = joblib.load(open("./models/scaler.pkl","rb"))
print('Scaler Model Loaded')
university = joblib.load(open('./models/university.pkl','rb'))
print('Naive Model Loaded')
linear_model = joblib.load(open('./models/linear_model.pkl','rb'))
print('Linear Model loaded')

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
        toefl = request.form.get('toefl')
        sop = request.form.get('sop')
        lor = request.form.get('lor')
        cgpa = request.form.get('cgpa')
        gre = request.form.get('gre')
        rating = request.form.get('rating')
        researchs = request.form.get('researchs')
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
        elif researchs =='Research':
                researchs = 1
        elif researchs == 'No Research':
            researchs = 0          
            
            
        
           
        if g.record ==1:
            
                # input_lst = [gre,toefl,rating,sop,lor,cgpa,researchs]
            new_input = {
                'GRE Score':gre,
                'TOEFL Score' :toefl,
                'University Rating':rating,
                'SOP':sop,
                'LOR' : lor,
                'CGPA':cgpa,
                'Research':researchs    
                }
            print(new_input)
            def predict_input(input):
                input_df = pd.DataFrame([input])
                print(input_df)
                input_df[input_df.columns] = scaler.transform(input_df[input_df.columns])
                print(input_df)
                if model == 'linear':
                    pred = linear_model.predict(input_df)
                else:
                    pred = university.predict(input_df)
                return pred
                
            prediction = predict_input(new_input)
            if model =='naivebayes':
                if prediction == 1:
                    send_email(g.email)
                    return render_template('success.html')
                elif prediction ==0:
                    fail_mail(g.email)
                    return render_template('fail.html')
                
            elif model == 'linear':
                predict = prediction * 100
                linear_mail(g.email,predict)
                return render_template('lineat_output.html',prediction= f'{predict}%')
            
        elif g.record == 0:
                # input_lst = [gre,toefl,rating,sop,lor,cgpa,researchs]
            new_input = {
                'GRE Score':gre,
                'TOEFL Score' :toefl,
                'University Rating':rating,
                'SOP':sop,
                'LOR' : lor,
                'CGPA':cgpa,
                'Research':researchs    
                }
            print(new_input)
            def predict_input(input):
                input_df = pd.DataFrame([input])
                print(input_df)
                input_df[input_df.columns] = scaler.transform(input_df[input_df.columns])
                print(input_df)
                if model == 'linear':
                    pred = linear_model.predict(input_df)
                else:
                    pred = university.predict(input_df)
                return pred
                
            prediction = predict_input(new_input)
            if model =='naivebayes':
                if prediction == 1:
                    return render_template('success.html')
                elif prediction ==0:
                    return render_template('fail.html')
                
            elif model == 'linear':
                predict = prediction *100
                return render_template('lineat_output.html',prediction= f'{predict}%')
            
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