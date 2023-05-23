from ToolModule import GetSession, JWTManager, json, jsonify, get_remote_address, Limiter, session, check_password_hash, GetModel, GetAllObjectsInModel, render_template, generate_password_hash, Flask, request, redirect, io, csv, GetTable
from ToolModule.Database import RemoveMultipleFromTable, InsertMultipleToTable, InsertToTable, RemoveFromTable, GetObjectFromTable, UpdateTable, GetRelatedTableFromForeignKey, InsertToTableWithoutSession
from ToolModule.htmlHelper import GetList, CheckIfLoggedOut
import requests, json, re, os
from ToolModule import deviceName, batchName, configName, customerName, firmwareName, keysName, ordersName, producersName, roleName, usersName, index, loginName, csvName, insertName, removeName

dir_path = '/home/ubuntu/config/'
filename = 'jwt'
file_path = os.path.join(dir_path, filename)

with open(file_path, 'r') as f:
    # Write the connection string to the file
    first_line = f.readline()

https = Flask(__name__)
jwt = JWTManager(https)
https.secret_key = 'hej'
https.config['SESSION_TYPE'] = 'filesystem'
https.config['SESSION_COOKIE_SECURE'] = True
https.config['JWT_SECRET_KEY'] = first_line

def is_valid_jwt(token):
    # JWT token format regular expression
    jwt_pattern = r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]*$'

    # Check if the token matches the JWT format
    if re.match(jwt_pattern, token):
        return True
    else:
        return False

@https.route('/administrator/all/<objects>/all/tools/getRelatedTable/<key_type>/<foreign_key>', methods=['GET'])
def get_foreign_key_table(objects, foreign_key, key_type):
    table = GetRelatedTableFromForeignKey(objects, foreign_key, key_type)
    if(str(table).startswith('(False') or table == False):
        return redirect(request.referrer)
    else:
        return redirect('/administrator/all/' + str(table) + '/all/tools/manager')

# App routes
@https.route(deviceName, methods=['GET'])
def DeviceList():
    return GetList('devices')

@https.route(batchName, methods=['GET'])
def BatchList():
    return GetList('batch')   

@https.route(customerName, methods=['GET'])
def CustomerList():
    return GetList('customers') 

@https.route(firmwareName, methods=['GET'])
def FirmwareList():
    return GetList('firmwares') 

@https.route(configName, methods=['GET'])
def ConfigList():
    return GetList('config') 

@https.route(keysName, methods=['GET'])
def KeyList():
    return GetList('rsakeys') 

@https.route(ordersName, methods=['GET'])
def OrderList():
    return GetList('orders') 

@https.route(producersName, methods=['GET'])
def ProducerList():
    return GetList('producers') 

@https.route(roleName, methods=['GET'])
def RoleList():
    return GetList('role') 

@https.route(usersName, methods=['GET'])
def UserList():
    return GetList('users') 

@https.route(index)
def Index():
    if 'user_id' in session:
        return render_template('toolindex.html')
    return 'Login required', 401

from datetime import timedelta

@https.route(loginName, methods=['POST', 'GET'])
def login():
    # retrieve form data from the HTTP request
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        userRow = GetObjectFromTable(user, 'users', 'name')
        # check if 'password' field is in the values dictionary
        if userRow is None or not check_password_hash(userRow.password, password):
            return 'Username or password incorrect', 401
        if userRow.role_id != 0:
            return 'Access Denied', 403
        session.permanent = True  # Enable session permanence
        https.permanent_session_lifetime = timedelta(minutes=30)  # Set session timeout to 30 minutes
        jwt_token = None
        headers = {'Content-Type': 'application/json'}
        data = {'name': user, 'password': password}
        response = requests.post('http://localhost:5001/login', headers=headers, json=data)
        try:
            json_data = response.json()  # Extract JSON data from the response
            if 'jwt' in json_data:
                jwt_token = json_data['jwt']  # Extract the JWT token from the JSON data
                print(jwt_token)
            # Now you can use the JWT token for further authentication/authorization
            else:
                print("JWT token not found in the response")
        except json.JSONDecodeError:
            # Handle the case when the response does not contain valid JSON
            print("Invalid JSON response")
        session['user_id'] = userRow.id
        session['jwt'] = jwt_token
        print(is_valid_jwt(session['jwt']))
        return redirect(index)
    
    if request.method == 'GET':
        return render_template('login.html')


@https.route(insertName, methods=['POST'])
def Insert(object):
    CheckIfLoggedOut()
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


@https.route(removeName, methods=['POST'])
def Remove(object):
    CheckIfLoggedOut()
    # Print the form data received in the request
    print(request.form)
    # Get a list of checkedIds from the form data
    values = request.form.getlist('checkedIds[]')
    json_data = json.dumps(values)
    # Print the list of selected values to verify that it is not empty
    print("Selected values:", values)
    if 'devices' in request.url:
        headers = {
        'Authorization': 'Bearer ' + session['jwt'].strip(),
        'Content-Type': 'application/json'
        }
        response = requests.post('http://localhost:5002/users/' + str(session['user_id']) + '/devices/' + str(values[0]) + '/keys/remove', headers=headers, data=json_data)
        if response.status_code != 200:
            return 'Error: ' + response.text, 500
    # Loop through the selected values and remove each from the table using the op.RemoveFromTable function
    RemoveMultipleFromTable(object, values)
    # Return a refreshed list of the remaining objects in the table
    return redirect('/administrator/all/'+ object +'/all/tools/manager'), 200

@https.route(csvName, methods=['POST'])
def Upload():
    CheckIfLoggedOut()
    # Try to get csvFile from name and tableName from form
    try:
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
                        columnType = GetTable(tableName).columns[columnName].type
                        convertedValue = columnType.python_type(row[i])
                        convertedRow[columnName] = convertedValue
                    except ValueError as e:
                        print(f"Error converting value '{row[i]}' to {columnType}: {e}")
                        return 'Error converting value', 500
                rows.append(convertedRow)
            InsertMultipleToTable(tableName, rows)
        return 'Upload successful', 200
    except Exception as e:
        print(e)
        return 'Error uploading CSV file', 500
    
@https.route("/administrator/all/<table_name>/all/tools/update", methods=["POST"])
def updateTableValues(table_name):
    UpdateTable(table_name)
    return 'Update Successful', 200
   

if __name__ == '__main__':
    https.run(ssl_context='adhoc', host='0.0.0.0', port=5000, debug=True)