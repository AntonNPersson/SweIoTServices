from AuthModule import  admin_required, loginName, protectName, check_password_hash, create_access_token, secretKey, tokenLocation, tokenExpire, secureCookie, Flask, request, jsonify, JWTManager, jwt_required, current_user
from AuthModule.Database import GetObjectFromTable, GetPasswordFromUsername
import os

dir_path = '/home/ubuntu/config/'
filename = 'jwt'
file_path = os.path.join(dir_path, filename)

with open(file_path, 'r') as f:
    # Write the connection string to the file
    first_line = f.readline()

https = Flask(__name__)
https.config["JWT_SECRET_KEY"] = first_line
#https.config["JWT_TOKEN_LOCATION"] = tokenLocation
#https.config["JWT_COOKIE_SECURE"] = secureCookie
#https.config["JWT_ACCESS_TOKEN_EXPIRES"] = tokenExpire
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
    username = request.form.get("name", None)
    password = request.form.get("password", None)
    user = GetObjectFromTable(username, 'users', 'name')
    if user is None or not check_password_hash(str(user.password), password):
        return 'Username or password incorrect', 401
    accessToken = create_access_token(identity=user.id)
    return jsonify(jwt=accessToken), 200
# Returns json pair - jwt: access token

# curl -X GET https://localhost:5000/protected -H "Authorization: Bearer <your_token>"
@https.route(protectName, methods=["GET"])
@jwt_required()
@admin_required
def protected():
    return jsonify(id=current_user.id, username=current_user.name)

if __name__ == '__main__':
    https.run(port=5001, host='0.0.0.0')