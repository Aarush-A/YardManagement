from flask import request, jsonify
from flask_restful import Resource
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

def connect():
    conn = sqlite3.connect('yard_management.db')
    return conn

class user_api(Resource):
    def get(self):
        data = request.get_json()
        user = data.get('employeeid')
        passw = data.get('password')
        conn = connect()
        cursor = conn.cursor()
        fetch = cursor.execute('SELECT * FROM User WHERE EmployeeID=? AND Password=?', (user, passw)).fetchone()
        conn.close()
        if fetch:
            return {'message': 'Login Successful'}, 200
        else:
            return {'message': 'Invalid Credentials'}, 401

    def post(self):
        data = request.get_json()
        user = data.get('employeeid')
        passw = data.get('password')
        name = data.get('name')
        role=data.get('role')
        conn = connect()
        cursor = conn.cursor()
        fetch = cursor.execute('SELECT * FROM User WHERE EmployeeID=?', (user)).fetchall()
        if fetch:
            conn.close()
            return {'message': 'User already registered'}, 400
        else:
            cursor.execute('INSERT INTO User (EmployeeID, Name, Role, Password) VALUES (?, ?, ?, ?)', (user, name, passw, role))
            conn.commit()
            conn.close()
            return {'message': 'Registration successful'}, 200