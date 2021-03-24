from flask import Flask,render_template


app = Flask(__name__)
app.config.from_object('config')


@app.route('/index')
def index():
    data = [1,3,4,5,6]


    return render_template('index.html',data=data)




























