from flask import Flask, render_template, request, redirect
from datetime import datetime


app = Flask(__name__)
app.app_context().push()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/arimkaji')
def arimkaji():
    return render_template('arimkaji.html')

@app.route('/rajukaju')
def rajukaju():
    return render_template('rajukaju.html')

@app.route('/riddhi')
def riddhi():
    return render_template('riddhi.html')

@app.route('/supro')
def supro():
    return render_template('supro.html')            
        
@app.route('/clasmate')
def clasmate():
    return render_template('clasmate.html')


if __name__ == '__main__':
    app.run(debug=True)