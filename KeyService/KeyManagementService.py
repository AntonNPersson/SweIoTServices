from KeyModule.Database import (
    AddKeyPairFromDevice, GetPrivateKeyFromID,
    GetPublicKeyFromID, RemoveKeyPairFromDevice,
    RemoveMultipleKeyPairFromDevice, is_mac_address, GetIdFromMacWithoutSession
)
from KeyModule.crypto import (
    RSAKeyGenerator, SignWithPrivateKey, ECCKeyGenerator, VerifyWithPublicKey
)

import os
from KeyModule import (
    removeKeyPairName, admin_required,
    device_ownership_required, more_itertools,
    Flask, jwt_required, JWTManager,
    CheckContentType, generatorName,
    signingName, splitSigningName,
    getPrName, getPuName, file_path, GetSession,
    GetSpecificFromColumnInTable, get_jwt_identity, jsonify,
    make_response, signMessageWithKey, verifyMessageWithKey
    )

with open(file_path, 'r') as f:
    # Write the connection string to the file
    first_line = f.readline()

https = Flask(__name__)
https.config["JWT_SECRET_KEY"] = first_line
jwt = JWTManager(https)

# curl -X POST -H "Content-Type: application/json" -d "{"key_type": "RSA"}" https://localhost:5000/users/123/devices/456/keys/generate -k
# Verify ownership, generate RSA key pair, add to database and then return public key  

@https.route(generatorName, methods=['POST'])
@jwt_required()
def GenerateKeysMain(user_id, device_id):
    try:
        private_key, public_key = ECCKeyGenerator()
        print(AddKeyPairFromDevice(private_key, public_key.encode(), deviceId=device_id))
        if private_key and public_key:
            response = {
                "private_key": private_key.decode('utf-8'),
                "public_key": public_key
            }
            r = make_response(jsonify(response), 200)
            r.headers['Content-Type'] = 'application/json'
            return r
        else:
            response = {"error": "Failed to generate keys"}
            r = make_response(jsonify(response), 500)
            r.headers['Content-Type'] = 'application/json'
            return r
    except Exception as e:
        response = {"error": str(e)}
        r = make_response(jsonify(response), 500)
        r.headers['Content-Type'] = 'application/json'
        return r

        
@https.route(removeKeyPairName, methods=['POST'])
@admin_required
def RemoveKeyPairMain(user_id, device_id):
    data = CheckContentType()
    if(len(data['deviceIds']) > 1):
        return RemoveMultipleKeyPairFromDevice(data['deviceIds']), 200
    else:
        return RemoveKeyPairFromDevice(device_id), 200

# need to add verification if the device belongs to user with jwt token
# curl -X GET http://yourdomain:5000/users/1234/devices/5678/private
@https.route(getPrName, methods=['GET'])
@jwt_required()
@admin_required
def GetPrKeyMain(user_id, device_id):
    return GetPrivateKeyFromID(device_id), 200

# need to add verification if the device belongs to user with jwt token
# curl -X GET http://yourdomain:5000/users/1234/devices/5678/public    
@https.route(getPuName, methods=['GET'])
@jwt_required()
def GetPuKeyMain(user_id, device_id):
    db, base = GetSession()
    userid = get_jwt_identity()
    customer = GetSpecificFromColumnInTable(db, base, userid, 'customer_id', 'users')
    if is_mac_address(device_id):
        device_id = GetIdFromMacWithoutSession(device_id, db, base)
    device = GetSpecificFromColumnInTable(db, base, device_id, 'customer_id', 'devices')
    if device is None or device != customer:
        db.close()
        return 'Device does not belong to user', 400
    try:
        publicKey = GetPublicKeyFromID(device_id, db, base)
        db.close()
        if publicKey is None:
            return 'No public key found for device with ID: ' + device_id, 404
        else:
            response = {"public_key": str(publicKey)}
            r = make_response(jsonify(response), 200)
            r.headers['Content-Type'] = 'application/json'
            return r
    except Exception as e:
        db.close()
        https.logger.error(e)
        return 'Error: Check Logs', 500

# curl -X POST -H "Content-Type: application/json" http://yourdomain:5000/users/1234/devices/5678/sign    
# Verify ownership, sign message with private key in database, hash the message and then return hashed message
from flask import make_response, jsonify

@https.route(signingName, methods=['POST'])
@jwt_required()
def SignMessageMain(user_id, device_id):
    db, base = GetSession()
    userid = get_jwt_identity()
    customer = GetSpecificFromColumnInTable(db, base, userid, 'customer_id', 'users')
    if customer is None:
        db.close()
        response = {"signed_message": "User does not exist"}
        return make_response(jsonify(response), 200, {'Content-Type': 'application/json'})
    if is_mac_address(device_id):
        device_id = GetIdFromMacWithoutSession(device_id, db, base)
    device = GetSpecificFromColumnInTable(db, base, device_id, 'customer_id', 'devices')
    if device is None:
        db.close()
        response = {"signed_message": "Device does not exist"}
        return make_response(jsonify(response), 200, {'Content-Type': 'application/json'})
    if device != customer:
        db.close()
        response = {"signed_message": "Device does not belong to user"}
        return make_response(jsonify(response), 200, {'Content-Type': 'application/json'})
    try:
        data = CheckContentType()
        if data:
            privateKey = GetPrivateKeyFromID(device_id, db, base)
            db.close()
            if privateKey is None:
                response = {'signed_message': 'No private key found for device with ID: ' + device_id}
                return make_response(jsonify(response), 200, {'Content-Type': 'application/json'})
            message = SignWithPrivateKey(privateKey, data['message'])
            if message is None:
                response = {'signed_message': 'Failed to sign message'}
                return make_response(jsonify(response), 500, {'Content-Type': 'application/json'})
            response = {"signed_message": message}
            return make_response(jsonify(response), 200, {'Content-Type': 'application/json'})
        else:
            response = {'signed_message': 'Failed to sign message'}
            return make_response(jsonify(response), 500, {'Content-Type': 'application/json'})
    except Exception as e:
        response = {"signed_message": str(e)}
        return make_response(jsonify(response), 500, {'Content-Type': 'application/json'})
    
# DEBUG METHODS
@https.route(signMessageWithKey, methods=['POST'])
def SignMessageWithKeyMain(user_id, device_id):
    data = CheckContentType()
    if data:
        message = SignWithPrivateKey(data['private_key'], data['message'])
        if message is None:
            response = {'signed_message': 'Failed to sign message'}
            return make_response(jsonify(response), 500, {'Content-Type': 'application/json'})
        response = {"signed_message": message}
        return make_response(jsonify(response), 200, {'Content-Type': 'application/json'})
    else:
        response = {'signed_message': 'Failed to sign message'}
        return make_response(jsonify(response), 500, {'Content-Type': 'application/json'})
    
@https.route(verifyMessageWithKey, methods=['POST'])
def VerifyMessageWithKeyMain(user_id, device_id):
    data = CheckContentType()
    if data:
        message = VerifyWithPublicKey(data['public_key'], data['message'], data['signature'])
        if not message:
            response = {'verified': False}
            return make_response(jsonify(response), 200, {'Content-Type': 'application/json'})
        response = {"verified": message}
        return make_response(jsonify(response), 200, {'Content-Type': 'application/json'})
    else:
        response = {'verified': False}
        return make_response(jsonify(response), 500, {'Content-Type': 'application/json'})

if __name__ == "__main__":
    https.run(port=5002, host='0.0.0.0')
    