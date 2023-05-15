from flask import Blueprint,redirect,url_for,render_template, request
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/')
def display():
    return render_template('index.html')

# accept submit btn
@main.route('/result', methods=['POST','GET'])
def submit():
    db = mysql.connector.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        ssl_ca=os.getenv("SSL_CERT")
    )
    cur = db.cursor()
    s = tuple(float(x) for x in request.form.getlist('inp'))
    cur.execute(f"INSERT INTO marks(science, maths, english, computer) VALUES{s}")
    db.commit()
    db.close()
    if request.form.get('result'):  #check from which source request came
        return render_template('result.html',marks=sum(s)/4)
    else:
        return render_template('percent.html',d = zip(['Science','Maths','English','Computer'],list(s)))

@main.route('/view')
def view():
    db = mysql.connector.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        ssl_ca=os.getenv("SSL_CERT")
    )
    cur = db.cursor()
    cur.execute("SELECT * FROM marks")
    userDetails = cur.fetchall()
    db.close()
    return render_template('marks.html', marks=userDetails)
