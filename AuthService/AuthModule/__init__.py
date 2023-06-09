from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token, get_current_user, JWTManager, jwt_required, current_user
)
from flask import jsonify, request, Flask, make_response
import os
from functools import wraps
from enum import Enum
from SIOTC import GetModel, executeQuery, admin_required
from SIOTC.helperhttps import device_ownership_required

loginName = '/login'
protectName = '/protected'
authDeviceName = '/administrator/<user_id>/devices/<device_id>/auth'

secretKey = os.environ.get('JWT_SECRET_KEY')
tokenLocation = os.environ.get('JWT_TOKEN_LOCATION')
secureCookie = os.environ.get('JWT_COOKIE_SECURE')
tokenExpire = 3600

fileName = 'jwt'
dir_path = '/home/ubuntu/config/'
file_path = os.path.join(dir_path, fileName)