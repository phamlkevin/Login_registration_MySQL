from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re
import md5

app = Flask(__name__)
app.secret_key = '22'
mysql = MySQLConnector(app,'login')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('index.html')


##################################### register #############################

@app.route('/register', methods=['POST'])
def register():

    email = request.form['email']                         
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    password_confirm = request.form['password_confirm']
    # check = True    # use this like a check list for all "if" statements

    # if len(email) < 1 or len(first_name) < 1 or len(last_name) < 1 or len(password) < 1 or len(password_confirm) < 1:
    #     flash("Everything needs to be filled")

    # if password != password_confirm:
    #     flash("Passwords do not match")
    #     check = False
    # if len(password) < 8:       # len can be used for anything, numbers and strings
    #     flash("Must be longer than 8 characters")
    #     check = False
    # if not first_name.isalpha() or not last_name.isalpha():  # .isalpha() a strings only comparssion!
    #     flash("Must be a-z or A-Z")
    #     check = False
    # if not EMAIL_REGEX.match(email):
    #     flash("Not vaild!")
    #     check = False

    # if check == True:
    #     flash("Success!")
    query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': request.form['password']
            }
    mysql.query_db(query, data)
    return redirect('/success')


@app.route('/success')
def success():
    return render_template('success.html')

##################################### register #############################








##################################### login #############################

@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']
    # hashed_password = md5.new(password).hexdigest()

    user_input = {
            'email': 'email',
            'password': 'password'
                }
    login_try = "SELECT * FROM users WHERE email = :email AND password = :password"

    query_attempt = mysql.query_db(user_input, login_try)

    # if query_attempt:
    #     flash("Login Successful")
    # else:
    #     flash("Invald login and password")
    # return redirect('/')


##################################### login#############################


app.run(debug=True)