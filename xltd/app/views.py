from flask_login import login_required
from flask import render_template,send_from_directory,request
from app import app
import os,time,json



@app.route('/css/<path:path>')
def send_css(path):
    #return send_from_directory(os.path.join(app.root_path, 'static/css'), path)
    return send_from_directory(app.static_folder+'/css', path)

@app.route('/js/<path:path>')
def send_js(path):
    #return send_from_directory(os.path.join(app.root_path, 'static/js'), path)
    return send_from_directory(app.static_folder + '/js', path)

@app.route('/font-awesome/<path:path>')
def send_font_awesome(path):
    #return send_from_directory(os.path.join(app.root_path, 'static/font-awesome'), path)
    return send_from_directory(app.static_folder + '/font-awesome', path)

@app.route('/bootstrap-dist/<path:path>')
def send_bootstrap_dist(path):
   # return send_from_directory(os.path.join(app.root_path, 'static/bootstrap-dist'), path)
   return send_from_directory(app.static_folder + '/bootstrap-dist', path)

@app.route('/img/<path:path>')
def send_img(path):
    #return send_from_directory(os.path.join(app.root_path, 'static/img'), path)
    return send_from_directory(app.static_folder + '/img', path)

@app.route('/pic/<path:path>')
def send_pic(path):
    #return send_from_directory(os.path.join(app.root_path, 'static/img'), path)
    return send_from_directory(app.static_folder + '/pic', path)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/')
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/breaker_index')
@login_required
def breaker_index():
    return render_template("breaker_index.html")

@app.route('/auto_dust')
def auto_dust():
    pm_confg = json.load(open('D:/pythonweb/app/mod_zthr/pm.json', 'r', encoding='utf-8'))
    pm_max = pm_confg['max']
    pm_min = pm_confg['min']
    return render_template("autodust.html",maxdust=pm_max,mindust=pm_min)


#update pm.json
@app.route('/autodust_updatejson',methods=['POST'])
def update_json():
    _max = request.form['maxdust']
    _min = request.form['mindust']
    print('ddddddddddddd===============', _max,'--',_min)
    _data = {'max':int(_max),'min':int(_min)}

    with open('D:/pythonweb/app/mod_zthr/pm.json', 'w') as f:
        f.write(json.dumps(_data))

    return render_template("autodust.html", maxdust=_max, mindust=_min)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('error_404.html'), 404
