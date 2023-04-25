from ToolModule import jsonify, get_remote_address, Limiter, session, check_password_hash, GetModel, GetAllObjectsInModel, render_template, generate_password_hash, Flask, request, redirect, io, csv, GetTable
from ToolModule.Database import InsertToTable, RemoveFromTable, GetObjectFromTable, UpdateTable, GetRelatedTableFromForeignKey
from ToolModule.htmlHelper import GetList
from ToolModule import deviceName, batchName, configName, customerName, firmwareName, keysName, ordersName, producersName, roleName, usersName, index, loginName, csvName, insertName, removeName

https = Flask(__name__)
https.secret_key = 'hej'

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
        session['user_id'] = userRow.id
        return redirect(index)
    if request.method == 'GET':
        return render_template('login.html')

@https.route(insertName, methods=['POST'])
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
    InsertToTable(object, values) 
    # print the form data to the console
    print(values)
    # return a list of all records in the specified table
    return redirect('/administrator/all/'+ object +'/all/tools/manager'), 200

@https.route(removeName, methods=['POST'])
def Remove(object):
    # Print the form data received in the request
    print(request.form)
    # Get a list of checkedIds from the form data
    values = request.form.getlist('checkedIds[]')
    # Print the list of selected values to verify that it is not empty
    print("Selected values:", values)
    # Loop through the selected values and remove each from the table using the op.RemoveFromTable function
    for value in values:
        RemoveFromTable(object, value)
    # Return a refreshed list of the remaining objects in the table
    return redirect('/administrator/all/'+ object +'/all/tools/manager'), 200

@https.route(csvName, methods=['POST'])
def Upload():
    # Try to get csvFile from name and tableName from form
    try:
        csvFile = request.files['csvFile']
        tableName = request.form['tableName']
        # Use StringIO for reading file
        with io.StringIO(csvFile.stream.read().decode("UTF8"), newline='') as csvf:
            reader = csv.reader(csvf)
            # Read first row and set columnNames
            columnNames = next(reader)  
            data = []
            for row in csv.DictReader(csvf, fieldnames=columnNames):
                convertedRow = {}
                for columnName in columnNames:
                    try:
                        columnType = GetTable(tableName).columns[columnName].type # Get Datatype of column
                        convertedValue = columnType.python_type(row[columnName]) # Convert variable to Datatype with value
                        convertedRow[columnName] = convertedValue # Set row to convertedValue
                    except ValueError as e:
                        print(f"Error converting value '{row[columnName]}' to {columnType}: {e}")
                        return 'Error converting value', 400
                InsertToTable(tableName, convertedRow)
        return 'Upload successful', 200
    except Exception as e:
        print(e)
        return 'Error uploading CSV file', 400
    
@https.route("/administrator/all/<table_name>/all/tools/update", methods=["POST"])
def updateTableValues(table_name):
    UpdateTable(table_name)
    return 'Update Successful', 200
   

if __name__ == '__main__':
    https.run(ssl_context='adhoc')