# Packages
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask import Flask, jsonify, Response, make_response
from SIOTC.Operations import (
    GetAllFromTable, GetFromTable, GetTable, GetAllObjectsInModel, GetSpecificFromColumnInTable
)
from SIOTC import GetModel, executeQuery, GetSession

import os


# Endpoints
lookUpAllName = '/users/<user_id>/devices/lookup/all'
ownsDeviceName = '/users/<user_id>/devices/<device_id>/ownsdev'
secDeviceName = '/users/<user_id>/devices/<device_id>/secdev'

# Configuration
dir_path = '/home/ubuntu/config/'
filename = 'jwt'
file_path = os.path.join(dir_path, filename)