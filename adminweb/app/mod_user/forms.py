from app import app,login
from flask_login import login_required ,current_user,login_user,logout_user
from flask import render_template,request, session,redirect,flash,url_for
import app.mod_user.service as c
from app.mod_user.models import User
import datetime,hashlib,copy



#导航页面里的href上使用 <a class="" href="{{ url_for('list_all_users') }}"> 或  href="/userlist"都可以路由到这里
@app.route('/user/list')
@login_required
def list_all_users():
    user = c.get_all_data()
    return render_template("user/userlist.html", userlist=user)


@app.route('/user/edit/<int:id>')
@login_required
def edit_user(id):
    selectuser = User()
    if (id != 0):
        selectuser = c.select_by_id(id)
    else:
        selectuser.id = 0

    print(selectuser)
    return render_template("user/userform.html",selectuser= selectuser)


@app.route('/user/save',methods=['POST'])
@login_required
def save_user():
    user = User()
    user.username = request.form['username']
    user.real_name = request.form['realname']
    user.theme = request.form['theme']
    user.id = int(request.form['data_id'])
    created = request.form['created']

    _id = user.id

    if created is not None:
        # user.created =  datetime.datetime.strptime(created, "%Y-%m-%d")
        user.created = datetime.datetime.strptime(str(created)[0:10],'%Y-%m-%d')
    #avoid missing value
    _user = copy.copy(user)

    _user.id = c.update_insert_data(user)
    flash(f'用户保存成功!!', 'save_info')

    # if _user.id != 0:
    #     return render_template("user/userform.html", selectuser=user)

    # user = c.get_all_user()
    # return render_template("user/userlist.html", userlist=user)
    # return redirect('/user/list')
    return render_template("user/userform.html", selectuser=_user)

@app.route('/user/delete/<int:id>')
@login_required
def delete_user(id):
    c.delete_by_id(id)
    flash('信息删除成功!!', 'delete_info')
    # user = c.get_all_user()
    # return render_template("user/userlist.html", userlist=user, delete_info = '信息删除成功!!')
    # return redirect(url_for('list_all_users_delete',info='信息删除成功!!'))
    return redirect('/user/list')


@app.route('/')
@app.route('/login.html')
@app.route('/login', methods=['GET', 'POST'])
def do_login_do():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    password = request.form['password']
    user = c.select_by_password(email,password)


    if user:
        login_user(user)
        session['userid'] = user.id
        # set session timeout
        session.permanent = True
        app.permanent_session_lifetime = datetime.timedelta(minutes=30)

        return redirect('index')


    flash('无效的用户名和密码！！','error')
    return render_template("login.html")
    #return render_template("error_auth.html")

@app.route('/logout')
def do_logout():
    session.clear()
    logout_user()
    return redirect("login")

@login.unauthorized_handler
def unauthorized_handler():
    #return 'Unauthorized'
    return render_template("500.html")


@login.user_loader
def user_loader(_id):
    return c.select_by_id(_id)

def md5(_password):
    _p = hashlib.md5()
    _p.update(bytes(_password,encoding='utf-8'))
    return _p.hexdigest()


