from flask import Flask,render_template,jsonify,url_for,redirect


app = Flask(__name__)
app.config.from_object('config')


@app.route('/index')
def index():
    data = [1,3,4,5,6]
    return render_template('index.html',data=data)


@app.route("/user/<user_name>")
def user_info(user_name):
    return f'hello {user_name}'

























