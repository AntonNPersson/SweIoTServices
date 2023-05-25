from KeyModule.Database import (
    AddKeyPairFromDevice, GetPrivateKeyFromID,
    GetPublicKeyFromID, RemoveKeyPairFromDevice,
    RemoveMultipleKeyPairFromDevice, is_mac_address, GetIdFromMacWithoutSession
)
from KeyModule.crypto import (
    RSAKeyGenerator, SignWithPrivateKey, ECCKeyGenerator
)

import os
from KeyModule import (
    removeKeyPairName, admin_required,
    device_ownership_required, more_itertools,
    Flask, jwt_required, JWTManager,
    CheckContentType, generatorName,
    signingName, splitSigningName,
    getPrName, getPuName, file_path, GetSession,
    GetSpecificFromColumnInTable, get_jwt_identity
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
@admin_required
def GenerateKeysMain(user_id, device_id):
        private_Key, public_Key = ECCKeyGenerator()
        print(public_Key, private_Key)
        return AddKeyPairFromDevice(private_Key, public_Key, device_id), 200
        keyPair = AddKeyPairFromDevice(private_Key, public_Key, device_id)
        if keyPair is None:
            return 'Failed to generate key-pair for device:: ' + device_id, 500
        else:
            return AddKeyPairFromDevice(private_Key, public_Key, device_id), 200
        
@https.route(removeKeyPairName, methods=['POST'])
@jwt_required()
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
            return 'No public key found for device with ID: ' + device_id, 200
        else:
            return publicKey, 200
    except Exception as e:
        db.close()
        https.logger.error(e)
        return 'Error: Check Logs', 500

# curl -X POST -H "Content-Type: application/json" http://yourdomain:5000/users/1234/devices/5678/sign    
# Verify ownership, sign message with private key in database, hash the message and then return hashed message
@https.route(signingName, methods=['POST'])
@jwt_required()
def SignMessageMain(user_id, device_id):
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
        data = CheckContentType()
        if(data):
            privateKey = GetPrivateKeyFromID(device_id, db, base)
            db.close()
            if(privateKey is None):
                return 'No private key found for device with ID: ' + device_id, 200
            message = SignWithPrivateKey(privateKey, data['message'])
            if(message is None):
                return 'Failed to sign message', 200
            response = {"signed_message": message}
            return response, 200
        else:
            return 'Wrong Content type', 400
    except Exception as e:
        https.logger.error(e)
        return 'Error: Check Logs', 500
if __name__ == "__main__":
    https.run(port=5002, host='0.0.0.0')
    