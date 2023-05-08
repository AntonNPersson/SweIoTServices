import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ec
from cryptography.hazmat.primitives import serialization, hashes
import base64
import more_itertools
from SIOTC import executeQuery, GetKeys, Devices, CheckContentType
from SIOTC.helperhttps import admin_required, device_ownership_required
from flask import Flask
from flask_jwt_extended import jwt_required, JWTManager

generatorName = '/users/<user_id>/devices/<device_id>/keys/generate'
signingName = '/users/<user_id>/devices/<device_id>/keys/sign'
splitSigningName = '/users/<user_id>/devices/<device_id>/keys/splitSign'
getPuName = '/users/<user_id>/devices/<device_id>/keys/public'
getPrName = '/users/<user_id>/devices/<device_id>/keys/private'