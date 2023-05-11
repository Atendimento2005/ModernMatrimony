from flask import Flask,redirect,url_for,render_template,request

app = Flask(__name__) 

@app.route('/')
def display():
    return render_template('index.html')

# accept submit btn
@app.route('/result', methods=['POST','GET'])
def submit():
    s = sum(int(x) for x in request.form.getlist('inp'))/4
    return render_template('result.html',marks=s)

#accept percentage btn
@app.route('/percentage', methods=['POST','GET'])
def percent():
    marks = request.form.getlist('inp')
    d = zip(['Science','Maths','English','Computer'],marks)
    return render_template('percent.html',d=d)

if __name__ =='__main__':
    app.run(debug=False,host='0.0.0.0')