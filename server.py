from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re #check for valid email
import md5 #use md5 hashing

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #email format
NAME_REGEX= re.compile(r'[a-zA-Z]') #name format

app = Flask(__name__)
mysql = MySQLConnector(app, 'login')
app.secret_key="22"


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")



@app.route('/login', methods=['POST'])
def login():
    password= md5.new(request.form['password']).hexdigest()
    email=request.form['email']
    select_query= "SELECT * FROM users WHERE users.email= :email AND users.password=:password"
    query_data={
                'email':email, 
                'password':password
                }
    user= mysql.query_db(select_query,query_data)
    if user: 
        return redirect('/success')
    else:
        flash("user Email or password invalid")
    return redirect('/')




@app.route('/register', methods=['POST'])
def namevalid():
    if len(request.form['first_name'])<2:
        flash("Name must be at least 2 characters long", category="name")
    if len(request.form['email'])<1:
        flash("Email cannot be blank!", category="email")
    if len(request.form['password'])<8:
        flash("Password must be at least 8 characters long")
    if request.form['confirm_password']==request.form['password']:
        flash("Password does not match")
    if not NAME_REGEX.match(request.form['first_name']):
        flash("Name must be letters only")
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
    else:
        first_name= request.form['first_name']
        last_name= request.form['last_name']
        email= request.form['email']
        password= md5.new(request.form['password']).hexdigest()
        insert_query="INSERT INTO users(first_name,last_name,email,password,created_at,updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
        query_data={
                    'first_name':first_name,
                    'last_name':last_name, 
                    'email':email, 
                    'password':password
                    }
        mysql.query_db(insert_query,query_data)
        return redirect('/success')
    return redirect('/')




@app.route('/success')
def success():
    return render_template("success.html")

app.run(debug=True)
