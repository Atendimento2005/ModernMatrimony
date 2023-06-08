from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from datetime import datetime
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

db = mysql.connector.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        ssl_ca=os.getenv("SSL_CERT")
    )

cur = db.cursor()

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)
app.app_context().push()


@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/dbtest')
def dbtest():
    cur.execute("SELECT * FROM Users")
    testData = cur.fetchall()
    return testData

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/registration2')
def registration2():
    return render_template('registration2.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/interests')
def interests():
    return render_template('interests.html')

@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/form')
def form():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)

