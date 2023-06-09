from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from datetime import datetime, date
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cur.execute(f"SELECT (id) FROM Users WHERE email = '{request.form.get('email')}' AND password = '{request.form.get('password')}'")
        account_id = cur.fetchone()
        if account_id:
            session['id'] = account_id[0]
            return redirect('/home')
        
        flash('Invalid Credentails', 'error')
        return redirect('/login')
    
    if session.get('id'):
        return redirect('/home')
    
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
    if session.get('id'):
        cur.execute(f"SELECT name, age, bio FROM Users WHERE id = {int(session.get('id'))}")
        user_data = cur.fetchone()
        return render_template('homepage.html', name = user_data[0], age = user_data[1], bio = user_data[2])
    return redirect('/login')

@app.route('/form', methods = ['GET', 'POST'])
def form():
    if request.method == 'POST':
        formData = request.form
        data = (
            formData.get('f_name').strip() + ' ' + formData.get('l_name').strip(),
            (date.today() - date.fromisoformat(formData.get('dob'))).days//365,
            formData.get('gender').strip()[0].upper(),
            formData.get('religion').strip(),
            formData.get('caste').strip(),
            formData.get('education').strip(),
            formData.get('city').strip(),
            1 if formData.get('date') == 'on' or formData.get('not-sure') else 0,
            1 if formData.get('marry') == 'on' or formData.get('not-sure') else 0,
            formData.get('interests'),
            'bio bio biobiobiobiobiobiobiobiobiobiobiobiobiobiobiobiobiobiobiobiobio',
            formData.get('email').strip(),
            formData.get('ph').strip(),
            formData.get('occupation').strip(),
            formData.get('alma').strip(),
            formData.get('password').strip()
        )
        cur.execute(f'''INSERT INTO Users(
                    name, 
                    age, 
                    sex, 
                    religion, 
                    caste, 
                    education, 
                    city, 
                    dating, 
                    marriage, 
                    interests, 
                    bio, 
                    email, 
                    ph, 
                    occupation, 
                    alma,
                    password
        )
        VALUES {data};''')
        db.commit()
        return 'updated DB!'
    
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)

