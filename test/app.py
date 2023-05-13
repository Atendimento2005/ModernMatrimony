from flask import Flask,redirect,url_for,render_template, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__) 

# configure db
db = yaml.load(open('db.yaml'), Loader = yaml.Loader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def display():
    return render_template('index.html')

# accept submit btn
@app.route('/result', methods=['POST','GET'])
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

@app.route('/view')
def view():
    cur = mysql.connection.cursor()
    result_Value = cur.execute("SELECT * FROM  marks")
    if result_Value > 0:
        userDetails = cur.fetchall()
        return render_template('marks.html', marks=userDetails)


if __name__ =='__main__':
    app.run(debug=False)