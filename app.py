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

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        session['email'] = request.form.get('email')
        return redirect('/home')
    
    if session.get('name'):
        return redirect('/home')

    return render_template('login.html')

@app.route('/home')
def home():
    if not session.get('name'):
        return redirect('/login')
    return render_template('home.html', email=session.get('email'))

if __name__ == '__main__':
    app.run(debug=True)