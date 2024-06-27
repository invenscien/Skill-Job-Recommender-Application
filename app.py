from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

  
app = Flask(__name__)
  
app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=xrd94478;PWD=46iFVYdKdJ5HiiWy",'','')

@app.route('/')

def homer():
    return render_template('index.html')


@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

        

   
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        
        password = request.form['password']
        email = request.form['email']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, password)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/dashboard')
def dash():
    
    return render_template('dashboard.html')

@app.route('/apply',methods =['GET', 'POST'])
def apply():
     msg = ''
     if request.method == 'POST' :
         username = request.form['username']
         email = request.form['email']
         qualification= request.form['qualification']
         skills = request.form['skills']
         jobs = request.form['s']
         company=request.form['c']
         sql = "SELECT * FROM job WHERE username =?"
         stmt = ibm_db.prepare(conn, sql)
         ibm_db.bind_param(stmt,1,username)
         ibm_db.execute(stmt)
         account = ibm_db.fetch_assoc(stmt)
         print(account)
         if account:
            msg = 'there is only 1 job position! for you'
            return render_template('apply.html', msg = msg)
         else:
            insert_sql = "INSERT INTO  job VALUES (?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, qualification)
            ibm_db.bind_param(prep_stmt, 4, skills)
            ibm_db.bind_param(prep_stmt, 5, jobs)
            ibm_db.bind_param(prep_stmt, 6, company)
            ibm_db.execute(prep_stmt)
         msg='You have successfully applied for the job'
     elif request.method == 'POST':
         msg = 'Please fill out the Application !'
     return render_template('apply.html', msg = msg)

@app.route('/display')
def display():
   
        arr = []
        sql = "SELECT * FROM job"
        stmt = ibm_db.exec_immediate(conn,sql)
        dictionary = ibm_db.fetch_assoc(stmt)
        while dictionary != False:
         inst={}
         inst['USERNAME']=dictionary['USERNAME']
         inst['EMAIL']=dictionary['EMAIL']
         inst['QUALIFICATION']=dictionary['QUALIFICATION']
         inst['SKILLS']=dictionary['SKILLS']
         inst['S']=dictionary['JOB']
         inst['C']=dictionary['COMPANY']
         arr.append(inst)
         dictionary = ibm_db.fetch_assoc(stmt) 
        print(arr)
        return render_template('display.html',arr=arr)
    

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   return render_template('index.html')


    
if __name__ == '__main__':
   app.run(host="0.0.0.0",port=8080)