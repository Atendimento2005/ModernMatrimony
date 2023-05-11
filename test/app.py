from flask import Flask,redirect,url_for,render_template,request

app = Flask(__name__) 

@app.route('/')
def display():
    return render_template('index.html')

# accept form post
@app.route('/formsubmit', methods=['POST','GET'])
def submit():
    a,b,c,d = request.form['Science'],request.form['Maths'],request.form['English'],request.form['Computer']
    s = eval(f'{a} + {b} + {c} + {d}')/4
    return redirect(url_for('Result',marks=s))

@app.route('/Result/<int:marks>')
def Result(marks):
    return render_template('result.html',marks=marks)


if __name__ =='__main__':
    app.run(debug=True)