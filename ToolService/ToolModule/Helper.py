from ToolModule import session, GetAllObjectsInModel, GetModel, redirect, render_template, GetSession, decode_token
from ToolModule import loginName, index
from flask import request
from datetime import datetime, timedelta, timezone
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            session.clear()
            return redirect(loginName)
        if is_token_expired(session['jwt']):
            session.clear()
            return redirect(loginName)
        return f(*args, **kwargs)
    return decorated_function

def secure_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] == True:
            return redirect(index)
        if 'login_tries' not in session:
            session['login_tries'] = 0
        if 'login_locked' in session and session['login_locked'] == True:
            if datetime.now(timezone.utc) > session['login_tries_expire'].replace(tzinfo=timezone.utc):
                session['login_locked'] = False
                session['login_tries'] = 0
            else:
                return 'Too many login attempts. Please try again later.', 403
        if session['login_tries'] >= 3:
            session['login_locked'] = True
            session['login_tries_expire'] = datetime.now(timezone.utc) + timedelta(minutes=5)
            return 'Too many login attempts. Please try again later.', 403
        return f(*args, **kwargs)
    return decorated_function

def is_token_expired(token):
    try:
        decoded_token = decode_token(token)
        exp = decoded_token['exp']  # Extract the expiration time from the token payload
        current_time = datetime.utcnow()  # Get the current UTC timestamp
        current_time_converted = int(current_time.timestamp())  # Convert the current time to a timestamp
        return current_time_converted > exp  # Compare the current time with the token's expiration time
    except Exception as e:
        # Handle the exception if decoding fails
        print(f"Error decoding token: {e}")
        return True

def GetList(name):
        dbsession, base = GetSession()
        # Get all items in the model with the specified name using the operation module
        try:
            items = GetAllObjectsInModel(name, dbsession, base)
        except:
            return 'Error: Cannot find table with name: ' + name
        # Create a list to store dictionaries representing the items
        itemsDict = []
        # Iterate through each item and convert it to a dictionary
        try:
            for item in items:
                itemDict = item.__dict__   # Convert the item to a dictionary
                itemDict.pop('_sa_instance_state', None)   # Remove the '_sa_instance_state' key from the dictionary
                itemsDict.append(itemDict)   # Append the dictionary to the itemsDict list
        except:
            return 'Error: Cannot convert items to dictionary'
        # Get the keys of the first dictionary in the itemsDict list, which represent the columns of the table
        columns = itemsDict[0].keys()
        # Get the model object for the specified name
        model = GetModel(name, dbsession, base)
        # Render the 'tableList2.html' template with the itemsDict list, columns, and model as arguments
        dbsession.close()
        return render_template('tableList2.html', items=itemsDict, columns=columns, orders=model)