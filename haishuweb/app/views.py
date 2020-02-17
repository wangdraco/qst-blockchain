#from flask_login import login_required
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

@app.route('/fonts/<path:path>')
def send_fonts(path):
    #return send_from_directory(os.path.join(app.root_path, 'static/font-awesome'), path)
    return send_from_directory(app.static_folder + '/fonts', path)

@app.route('/bootstrap-dist/<path:path>')
def send_bootstrap_dist(path):
   # return send_from_directory(os.path.join(app.root_path, 'static/bootstrap-dist'), path)
   return send_from_directory(app.static_folder + '/bootstrap-dist', path)

@app.route('/images/<path:path>')
def send_images(path):
    #return send_from_directory(os.path.join(app.root_path, 'static/img'), path)
    return send_from_directory(app.static_folder + '/images', path)

@app.route('/bootstrap/<path:path>')
def send_pic(path):
    #return send_from_directory(os.path.join(app.root_path, 'static/img'), path)
    return send_from_directory(app.static_folder + '/bootstrap', path)

@app.route('/ext/<path:path>')
def send_ext(path):
    #return send_from_directory(os.path.join(app.root_path, 'static/img'), path)
    return send_from_directory(app.static_folder + '/ext', path)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('error_404.html'), 404
