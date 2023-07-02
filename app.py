from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from datetime import datetime, date,  timedelta
import os
from dotenv import load_dotenv
import mysql.connector
import helpers

load_dotenv()

db = mysql.connector.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER_NAME"),
        password=os.getenv("PASSWORD"),
        ssl_ca=os.getenv("SSL_CERT")
    )

cur = db.cursor()

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = "filesystem"
app.permanent_session_lifetime = timedelta(minutes=43200)
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
            if not request.form.get('remember'):
                session.permanent = False
            session['id'] = account_id[0]
            return redirect('/home')
        
        flash('Invalid Credentails', 'error')
        return redirect('/login')
    
    if session.get('id'):
        return redirect('/home')
    
    return render_template('login.html')

@app.route('/home')
def home():
    if session.get('id'):
        if not (session.get('name') and session.get('age') and session.get('bio') and session.get('interests')):
            user_data = helpers.fetchUserByID(db, int(session.get('id')), ('name', 'age', 'bio', 'interests'))
            session['name'] = user_data['name']
            session['age'] = user_data['age']
            session['bio'] = user_data['bio']
            session['interests'] = user_data['interests']
            
        relation_data = helpers.fetchReccomendations(db, int(session.get('id')))

        return render_template('homepage.html', 
                               id = session.get('id'),  
                               name = session.get('name'), 
                               age = session.get('age'), 
                               bio = session.get('bio'), 
                               interests=session.get('interests'), 
                               relation_data = relation_data
                               )
    
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
                    password)
        VALUES {data};''')
        db.commit()
        return 'updated DB!'
    
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)

