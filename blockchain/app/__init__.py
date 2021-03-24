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



@app.route("/image")
def main_image():
    return  "<img src='https://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png'>"

@app.route('/data')
def main_data():

    data = [
        {"id": 1, "username": "zhang", "age": 18},
        {"id": 2, "username": "ligang", "age": 17}
    ]
    return jsonify(data)

@app.route("/login")
def for_index():
    return redirect(url_for("index"))



















