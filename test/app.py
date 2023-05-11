from flask import Flask,redirect,url_for

app = Flask(__name__) 

@app.route('/<score>') ### Decorator
def hi(score):
    return 'Culpa sit pariatur ea proident sunt pariatur sint aliquip fugiat irure.' + score

@app.route('/a/<s>')
def func(s):
    return redirect(url_for(hi,score=s))

if __name__ =='__main__':
    app.run(debug=True)