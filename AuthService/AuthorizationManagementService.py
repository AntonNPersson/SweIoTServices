import os
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, current_user
)
from AuthModule import (
    admin_required, loginName, protectName,
    check_password_hash, secretKey, tokenLocation,
    tokenExpire, secureCookie, file_path
)
from AuthModule.Database import (
    GetObjectFromTable, GetPasswordFromUsername
)

with open(file_path, 'r') as f:
    # Write the connection string to the file
    first_line = f.readline()

https = Flask(__name__)
https.config["JWT_SECRET_KEY"] = first_line
https.config["JWT_TOKEN_EXPIRES"] = timedelta(seconds=tokenExpire)
jwt = JWTManager(https)

@jwt.user_identity_loader
def userIdentityLookup(user):
    print(user.id)
    return user.id

@jwt.user_lookup_loader
def userLookupCallback(jwtHeader, jwtData):
    identity = jwtData['sub']
    user = GetObjectFromTable(identity, 'users', 'id')
    return user

# Example: curl -k 
# -H "Content-Type: application/x-www-form-urlencoded" 
# -X POST -d "name=antoniot&password=3485780" 
# https://localhost:5000/login
@https.route(loginName, methods=["POST"])
def login():
    try:
        content = request.content_type
        if content != 'application/json':
            return 'Content type must be application/json', 400
        data = request.get_json()

        username = data.get("name")
        password = data.get("password")
        user = GetObjectFromTable(username, 'users', 'name')
        if user is None:
            return 'Username or password incorrect', 401 

        if user and not check_password_hash(str(user.password), password):
            return 'Username or password incorrect', 401

        accessToken = create_access_token(identity=user)
        return jsonify(jwt=accessToken), 200
    except (SQLAlchemyError, IntegrityError, ValueError, TypeError) as e:
        https.logger.error(e)
        return 'Error: Check Logs', 500

if __name__ == '__main__':
    https.run(port=5001, host='0.0.0.0')