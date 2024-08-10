from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from flask_restful import Api
from api import user_api,section_api, books_api, req_api, graphs_api, pdf_api
import requests as rq
import sqlite3

app = Flask(__name__)
app.secret_key = 'palampur_ftw'

def getdb():
    conn=sqlite3.connect('yard_management.db')
    return conn

api = Api(app)
api.add_resource(user_api, '/api/user')

#REGISTRATION LOGIC
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        form_data = {
        'employeeid': request.form['employeeid'],
        'name': request.form['name'],
        'password': request.form['password'],
        'role': request.form['role']
        }
        if rq.post(url=request.url_root+'/api/user', json=form_data).status_code == 201:
            return redirect(url_for('login'))
        else:
            error_message = "Employee already exists. Please choose a different employeeid."
            return render_template('register.html', error_message=error_message)
    return render_template('register.html')

#LOGIN LOGIC
@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        login={
            'employeeid': request.form['employeeid'],
            'password': request.form['password'],    
        }
        res=rq.get(request.url_root+'api/user', json=login)
        if res.status_code==200:
            session['employeeid']=login['employeeid']
            role_json = res.json()
            if role_json:
                role=role_json.get('role')
                if role=='admin':
                    return redirect(url_for('admindash'))
                else:
                    return redirect(url_for('userdash'))
            else:
                return render_template('login.html', err="Wrong employeeid Or Password")
        else:
            return render_template('login.html', err="Wrong employeeid Or Password")
    return render_template('login.html')

