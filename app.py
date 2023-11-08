from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from datetime import datetime, date,  timedelta
import os
from dotenv import load_dotenv
import mysql.connector
import helpers
import shutil

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

@app.route('/profile/<id>')
def profile(id):
    cur.execute(f"Select * from Users where id={id};")
    user = cur.fetchall()
    return render_template('profile.html', user=user[0], id = session.get('id') if session.get(id) else 0)

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

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if session.get('id'):
        if not (session.get('name') and session.get('age') and session.get('bio') and session.get('interests')):
            user_data = helpers.fetchUserByID(db, int(session.get('id')), ('name', 'age', 'bio', 'interests'))
            session['name'] = user_data['name']
            session['age'] = user_data['age']
            session['bio'] = user_data['bio']
            session['interests'] = user_data['interests']

        if request.method == "POST":
            formData = request.form
            s_input = formData.get("searchbar")
            amin_input = int(formData.get("age-min"))
            amax_input = int(formData.get("age-max"))
            in_input = formData.get("interests")
            c_input = formData.get("city")

            s_query = f"LOWER(name) LIKE '%{s_input.lower()}%' AND " if s_input else ''
            a_query = f"age BETWEEN {amin_input} and {amax_input} AND " if amin_input and amax_input else "age BETWEEN 18 and 60 AND "
            c_query = f"LOWER(city) LIKE '%{c_input.lower()}%' AND " if c_input else ''
            in_query = f"interests LIKE '{in_input}'" if in_input.count('1') > 0 else f"interests LIKE '_______________'"

            print(f'Select * from Users WHERE {s_query + a_query + c_query + in_query};')

            cur.execute(f'Select * from Users WHERE {s_query + a_query + c_query + in_query};')
            data = cur.fetchall()
            return render_template('search.html',data=data, id = session.get('id'))

        else:
            cur.execute('select * from Users ORDER BY name;')
            data = cur.fetchall()
            return render_template('search.html',data=data,id = session.get('id'))

    return redirect('/login')
    

@app.route('/register', methods = ['GET', 'POST'])
def register():
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
            1 if (formData.get('choice') == 'date' or formData.get('choice') == 'not-sure') else 0,
            1 if (formData.get('choice') == 'marry' or formData.get('choice') == 'not-sure') else 0,
            formData.get('interests'),
            formData.get('bio').strip(),
            formData.get('email').strip(),
            formData.get('ph').strip(),
            formData.get('occupation').strip(),
            formData.get('alma').strip(),
            formData.get('password').strip()
        )
        cur = db.cursor()
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
        print('db updated')
        
        cur.execute(f"SELECT * FROM Users WHERE email = '{data[11]}' AND password = '{data[15]}'")
        user = cur.fetchone()

				
			
        shutil.copy(os.path.abspath('static/images/profiles/0.webp'), os.path.abspath(f'static/images/profiles/{user[0]}.webp'))

        #creating new relations (recommendations)

        cur.execute(f'SELECT * FROM Users WHERE (age > {user[2]-10} AND age < {user[2]+10}) AND (dating = {user[8]} OR marriage = {user[9]}) AND id != {user[0]} AND sex != "{user[3]}";')
        relUsers = cur.fetchall()
        cur = db.cursor()
        # cur.execute(f'SELECT first_id, second_id FROM Relations WHERE first_id = {user[0]} OR second_id = {user[0]};')
        # relatedIDs = [x[0] if x[1] == user[0] else x[1] for x in cur.fetchall()]
        queries = []
        for relUser in relUsers:
            # if relUser[0] in relatedIDs: continue
            score = 0
            score += (10 - min(abs(relUser[2] - user[2]), 6))
            for i in range(4, 14):
                if i == 10:
                    for j in range(15):
                        if user[10][j] == relUser[10][j]:
                            score += 1
                elif i not in [8, 9, 10, 11, 12, 13]:
                    score += 3 if user[i].lower() == relUser[i].lower() else 0
            queries.append((user[0], relUser[0], score))
        if len(queries):
            cur = db.cursor()
            cur.execute(f'INSERT INTO Relations(first_id, second_id, score) VALUES {str(queries)[1:-1]};')
            db.commit()

        session.permanent = False
        session['id'] = user[0]
        return redirect('/home')
    
    return render_template('form.html')

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port=80)

