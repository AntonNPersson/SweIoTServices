from functools import wraps
from datetime import datetime, timedelta, timezone
import json
import io
import csv
import logging
import os
import re
import requests

from flask import Flask, request, redirect, jsonify, session, flash, render_template
from flask_limiter import Limiter
from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash, generate_password_hash

from ToolModule import (
    GetTable, GetSession,
    deviceName, batchName, configName, customerName, firmwareName,
    keysName, ordersName, producersName, roleName, usersName,
    index, loginName, csvName, insertName, removeName,
    permanenceExpireTime, cookieSameSite, cookieSecure, cookieHttpOnly, sqlAlchemyTrackModifications,
    file_path, changepasswordName
)

from ToolModule.Database import (
    RemoveFromTable, InsertToTable, GetObjectFromTable, GetRelatedTableFromForeignKey,
    UpdateTable, RemoveMultipleFromTable, InsertMultipleToTable, GetTableWithoutSession,
    InsertMultipleToTableWithoutSession, updateCellValueById, passwordCheckById
    )

from ToolModule.Helper import (
    GetList, secure_login, login_required
    )

with open(file_path, 'r') as f:
    # Write the connection string to the file
    first_line = f.readline()

https = Flask(__name__)
jwt = JWTManager(https)
https.secret_key = first_line
https.config['SESSION_COOKIE_SAMESITE'] = cookieSameSite
https.config['SESSION_COOKIE_SECURE'] = cookieSecure
https.config['SESSION_COOKIE_HTTPONLY'] = cookieHttpOnly
https.config['JWT_ACCESS_TOKEN_EXPIRES'] = permanenceExpireTime
https.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = sqlAlchemyTrackModifications
https.config['JWT_SECRET_KEY'] = first_line
https.config['LOGIN_VIEW'] = loginName

@https.route('/administrator/all/<objects>/all/tools/getRelatedTable/<key_type>/<foreign_key>', methods=['GET'])
def get_foreign_key_table(objects, foreign_key, key_type):
    table = GetRelatedTableFromForeignKey(objects, foreign_key, key_type)
    if(str(table).startswith('(False') or table == False):
        return redirect(request.referrer)
    else:
        return redirect('/administrator/all/' + str(table) + '/all/tools/manager')


from datetime import timedelta

@https.route(loginName, methods=['POST', 'GET'])
@secure_login
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        userRow = GetObjectFromTable(user, 'users', 'name')
        if userRow is None or not check_password_hash(userRow.password, password):
            session['login_tries'] += 1
            flash('Invalid username or password')
            return redirect(loginName)

        if userRow.role_id != 0:
            session['login_tries'] += 1
            flash('Access denied')
            return redirect(loginName)
        
        jwt_token = None
        headers = {'Content-Type': 'application/json'}
        data = {'name': user, 'password': password}
        response = requests.post('http://localhost:5001/login', headers=headers, json=data)

        try:
            json_data = response.json()
            jwt_token = json_data['jwt']
        except json.JSONDecodeError:
            print("Invalid JSON response")

        session.permanent = True
        https.permanent_session_lifetime = permanenceExpireTime
        session['jwt'] = jwt_token
        session['user_id'] = userRow.id
        session['login_tries'] = 0
        session['logged_in'] = True
        if 'jwt' not in session or session['jwt'] is None:
            session.clear()
            flash('Login failed. Please try again.')
            return redirect(loginName)
        if response.status_code == 200:
            flash('Logged in successfully.')
            return redirect(index)
    if request.method == 'GET':
        return render_template('login.html')


@https.route(insertName, methods=['POST'])
@login_required
def Insert(object):
    # retrieve form data from the HTTP request
    values = dict(request.form)
    id = values.get('id')
    if id is not None and id == '':
        values.pop('id', None)
    # check if 'password' field is in the values dictionary
    if 'password' in values:
        # replace the plain-text password value with its hashed version
        values['password'] = generate_password_hash(values['password'])
    # insert form data into the specified database table
    deviceID = InsertToTable(object, values) 
    # print the form data to the console
    response = None
    print(session['jwt'])
    if 'devices' in request.url:
        headers = {
        'Authorization': 'Bearer ' + session['jwt'].strip(),
        }
        response = requests.post('http://localhost:5002/users/' + str(session['user_id']) + '/devices/' + str(deviceID) + '/keys/generate', headers=headers)
        if response.status_code != 200:
            return 'Error: ' + response.text, 500
    print(values)
    # return a list of all records in the specified table
    return redirect('/administrator/all/'+ object +'/all/tools/manager'), 200

@https.route(changepasswordName, methods=['POST'])
@login_required
def ChangePassword():
    db, base = GetSession()
    response = updateCellValueById(session['user_id'], generate_password_hash(request.form['newPassword']), 'users', 'password', db, base)
    db.close()
    if response == None:
        return 'Error: ' + 'Check logs', 500
    session.clear()
    return redirect('/administrator/tools/login'), 200

@https.route(csvName, methods=['POST'])
@login_required
def Upload():
    # Try to get csvFile from name and tableName from form
    try:
        db, base = GetSession()
        csvFile = request.files['csvFile']
        tableName = request.form['tableName']
        # Use StringIO for reading file
        with io.StringIO(csvFile.stream.read().decode("UTF8"), newline='') as csvf:
            reader = csv.reader(csvf)
            # Read first row and set columnNames
            columnNames = next(reader)
            rows = []
            for row in reader:
                convertedRow = {}
                for i, columnName in enumerate(columnNames):
                    try:
                        columnType = GetTableWithoutSession(tableName, db, base).columns[columnName].type
                        convertedValue = columnType.python_type(row[i])
                        # Check if the column name is "password" and hash the value
                        if columnName == 'password':
                            convertedValue = generate_password_hash(convertedValue)
                        convertedRow[columnName] = convertedValue
                    except ValueError as e:
                        print(f"Error converting value '{row[i]}' to {columnType}: {e}")
                        return 'Error converting value', 500
                rows.append(convertedRow)
            InsertMultipleToTableWithoutSession(tableName, rows, db, base)

            # Generate keypair for each device added
            if 'devices' in request.url:
                headers = {
                    'Authorization': 'Bearer ' + session['jwt'].strip(),
                }
                for row in rows:
                    deviceID = row.get('id')
                    response = requests.post('http://localhost:5002/users/' + str(session['user_id']) + '/devices/' + str(deviceID) + '/keys/generate', headers=headers)
                    if response.status_code != 200:
                        return 'Error: ' + response.text, 500

        db.close()
        return 'Upload successful', 200
    except Exception as e:
        print(e)
        db.close()
        return 'Error uploading CSV file', 500
    
@https.route("/administrator/all/<table_name>/all/tools/update", methods=["POST"])
@login_required
def updateTableValues(table_name):
    UpdateTable(table_name)
    return 'Update Successful', 200

# App routes
@https.route(deviceName, methods=['GET'])
@login_required
def DeviceList():
    return GetList('devices')

@https.route(batchName, methods=['GET'])
@login_required
def BatchList():
    return GetList('batch')   

@https.route(customerName, methods=['GET'])
@login_required
def CustomerList():
    return GetList('customers') 

@https.route(firmwareName, methods=['GET'])
@login_required
def FirmwareList():
    return GetList('firmwares') 

@https.route(configName, methods=['GET'])
@login_required
def ConfigList():
    return GetList('config') 

@https.route(keysName, methods=['GET'])
@login_required
def KeyList():
    return GetList('rsakeys') 

@https.route(ordersName, methods=['GET'])
@login_required
def OrderList():
    return GetList('orders') 

@https.route(producersName, methods=['GET'])
@login_required
def ProducerList():
    return GetList('producers') 

@https.route(roleName, methods=['GET'])
@login_required
def RoleList():
    return GetList('role') 

@https.route(usersName, methods=['GET'])
@login_required
def UserList():
    return GetList('users') 

@https.route(index)
@login_required
def Index():
    return render_template('toolindex.html')
   

if __name__ == '__main__':
    https.run(ssl_context='adhoc', host='0.0.0.0', port=5000)