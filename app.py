import os
import random
from flask import Blueprint,render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


app.secret_key = ''
app.config['SECRET_KEY'] = '1234567890'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

db = SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    deviceid = db.Column(db.String(1000))

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def LoadUser(id):
    return User.query.get(int(id))

@app.route("/")
def index():
    return "Hello from my world!!!"

@app.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('userid')
    pwd = request.form.get('password')
    auto = True if request.form.get('auto') == '1' else False
    print(auto)

    user = User.query.filter_by(name=name).first()

    if user and auto is True:
        print('logged_in_auto')

    elif not user or not check_password_hash(user.password,pwd):
        return 'Please Check your Login details'

    login_user(user,remember=auto)

    load_dir = os.path.join(basedir , user.deviceid)
    json_file = open(load_dir + "\\save_data.json")
    loader = json.load(json_file)

    return loader

@app.route('/update', methods=['POST'])
def update_post():
    name = request.form.get('userid')
    save_data = request.form.get('savedata')
    user = User.query.filter_by(name=name).first()

    if not user:
        return 'Please Check your Login details'

    save_dir = os.path.join(basedir , user.deviceid)

    json_str = json.loads(save_data)
    dump = json.dumps(json_str)
    json_file = open(save_dir + "\\save_data.json" , "w")
    json_file.write(dump)
    json_file.close()

    return 'updated'

@app.route('/checkuser', methods=['POST'])
def check_user_test():
    deviceid = request.form.get('deviceid')
    save_data = request.form.get('savedata')
    
    user = User.query.filter_by(deviceid=deviceid).first()
    if not user:
        new_user = User(email=None,name='user' + str(random.randrange(1000,9999)),deviceid=deviceid,password=None)
        db.session.add(new_user)
        db.session.commit()

        save_dir = os.path.join(basedir , deviceid)

        os.mkdir(save_dir)

        json_str = json.loads(save_data)
        dump = json.dumps(json_str)
        json_file = open(save_dir + "\\save_data.json" , "w")
        json_file.write(dump)
        json_file.close()

        return new_user.name

    return user.name

@app.route('/linkaccount', methods=['POST'])
def signup_post_test():
    email = request.form.get('email')
    pwd = request.form.get('password')
    name = request.form.get('userid')
    deviceid = request.form.get('deviceid')

    cEmail = User.query.filter_by(email=email).first()
    if cEmail:
        return 'email exists'

    cName = User.query.filter_by(name=name).first()
    if cName:
        return 'username exists'

    user = User.query.filter_by(deviceid=deviceid).first()
    
    if user:
        user.email = email
        user.password = generate_password_hash(pwd,method='sha256')
        user.name = name
        db.session.commit()
        return 'linked' 

    return 'Please call check_user first'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logged_out'


if __name__ == '__main__':
    app.run()
