from flask import Blueprint,redirect,url_for,render_template, request
from flask_mysqldb import MySQL

main = Blueprint('main', __name__)

mysql = MySQL(main)

@main.route('/')
def display():
    return render_template('index.html')

# accept submit btn
@main.route('/result', methods=['POST','GET'])
def submit():
    cur = mysql.connection.cursor()
    s = tuple(float(x) for x in request.form.getlist('inp'))
    cur.execute(f"INSERT INTO marks(science, maths, english, computer) VALUES {s}")
    mysql.connection.commit()
    cur.close()
    if request.form.get('result'):  #check from which source request came
        return render_template('result.html',marks=sum(s)/4)
    else:
        return render_template('percent.html',d = zip(['Science','Maths','English','Computer'],list(s)))

@main.route('/view')
def view():
    cur = mysql.connection.cursor()
    result_Value = cur.execute("SELECT * FROM  marks")
    if result_Value > 0:
        userDetails = cur.fetchall()
        return render_template('marks.html', marks=userDetails)
