from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from datetime import datetime


app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)
app.app_context().push()


@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/registration2')
def registration2():
    return render_template('registration2.html')

if __name__ == '__main__':
    app.run(debug=True)