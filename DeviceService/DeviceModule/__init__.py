from flask import Flask, jsonify
from SIOTC.Operations import GetAllFromTable, GetFromTable, GetTable, GetAllObjectsInModel, GetSpecificFromColumnInTable
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from SIOTC import GetModel

lookUpAllName = '/users/<user_id>/devices/lookup/all'
ownsDeviceName = '/users/<user_id>/devices/<device_id>/ownsdev'