from flask import Flask, render_template, url_for, redirect, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)

app.secret_key = 'your secret key'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'usersdb'
  
mysql = MySQL(app) 

@app.route('/')
def root(): 
    return render_template('main.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form: 
        username = request.form['username'] 
        password = request.form['password'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM details WHERE username = %s AND password = %s', (username, password, )) 
        details = cursor.fetchone() 
        if details: 
            session['loggedin'] = True
            session['id'] = details['id'] 
            session['name'] = details['name'] 
            session['address'] = details['address']
            session['email'] = details['email']
            msg = 'Logged in successfully !'
            return render_template('profile.html', msg = msg)
        else: 
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg) 

@app.route('/logout') 
def logout(): 
    session.pop('loggedin', None) 
    session.pop('id', None) 
    session.pop('name', None) 
    session.pop('address', None)
    session.pop('email', None)
    return redirect('/') 
  

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form : 
        name = request.form['name']
        email = request.form['email']
        username = request.form['username'] 
        password = request.form['password'] 
        address = request.form['address']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM details WHERE username = %s', (username, )) 
        details = cursor.fetchone() 
        if details: 
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username): 
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            cursor.execute('INSERT INTO details (name, email,username, password, address) VALUES (%s, %s, %s, %s, %s)', (name, email, username, password, address)) 
            mysql.connection.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('new_account.html', msg = msg) 
