# Packages
import os
import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives import serialization
import more_itertools
from SIOTC import executeQuery, GetKeys, Devices, CheckContentType, GetModel, GetSession, GetSpecificFromColumnInTable
from SIOTC.helperhttps import admin_required, device_ownership_required
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity

# Endpoints
generatorName = '/users/<user_id>/devices/<device_id>/keys/generate'
removeKeyPairName = '/users/<user_id>/devices/<device_id>/keys/remove'
signingName = '/users/<user_id>/devices/<device_id>/keys/sign'
splitSigningName = '/users/<user_id>/devices/<device_id>/keys/splitSign'
getPuName = '/users/<user_id>/devices/<device_id>/keys/public'
getPrName = '/users/<user_id>/devices/<device_id>/keys/private'

# Configuration
dir_path = '/home/ubuntu/config/'
filename = 'jwt'
file_path = os.path.join(dir_path, filename)