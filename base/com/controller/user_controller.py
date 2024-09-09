from datetime import datetime
from passlib.context import CryptContext

from flask import Flask, render_template, request, redirect, url_for, session, make_response
from app import app

from base.com.vo.user_vo import UserVO
from base.com.dao.user_dao import UserDAO

pwd_context = CryptContext(schemes=['scrypt'], deprecated='auto')


@app.route('/')
def index():
    return render_template('user/login.html')


# @app.route('/open_login_page')
# def open_login():
#     return render_template('login.html')


@app.route('/home')
def home():
    return render_template('core/index.html')


@app.route('/open_upload')
def open_upload():
    return render_template('detection/upload.html')


@app.route('/open_register_page')
def open_register():
    return render_template('user/register.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = pwd_context.hash(password)

        userVO = UserVO()
        userDAO = UserDAO()

        userVO.username = username
        userVO.password = hashed_password
        userVO.created_on = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
        userVO.updated_on = datetime.now().strftime('%H:%M:%S %d/%m/%Y')

        userDAO.create_user(userVO)

        return render_template('user/login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        userVO = UserVO()
        userDAO = UserDAO()

        user_details = userDAO.get_user_by_username(username)
        if user_details:
            print("=====>", user_details)
            print("=====>", user_details.user_id)
            if user_details.username == username and pwd_context.verify(password, user_details.password):
                resp = make_response(render_template('core/index.html'))  # , user_id=user_details.user_id))
                resp.set_cookie('user_id', str(user_details.user_id))
                return resp
                # return render_template('core/index.html', user_id=user_details.user_id)
            else:
                return render_template('user/login.html', error='Invalid Credentials')


@app.route('/logout')
def logout():
    resp = make_response(render_template('user/login.html'))
    resp.set_cookie('user_id', '', expires=0)
    return resp