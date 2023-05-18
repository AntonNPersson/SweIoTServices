from KeyModule.Database import AddKeyPairFromDevice, GetPrivateKeyFromID, GetPublicKeyFromID
from KeyModule.crypto import RSAKeyGenerator, SignWithPrivateKey
import os
from KeyModule import device_ownership_required, more_itertools, Flask, jwt_required, JWTManager, CheckContentType, generatorName, signingName, splitSigningName, getPrName, getPuName

dir_path = '/home/ubuntu/config/'
filename = 'jwt'
file_path = os.path.join(dir_path, filename)

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
    private_Key, public_Key = RSAKeyGenerator()
    print(public_Key, private_Key)
    keyPair = AddKeyPairFromDevice(private_Key, public_Key, device_id)
    if keyPair is None:
        return 'Failed to generate key-pair for device:: ' + device_id, 401
    else:
        return AddKeyPairFromDevice(private_Key, public_Key, device_id), 200

# need to add verification if the device belongs to user with jwt token
# curl -X GET http://yourdomain:5000/users/1234/devices/5678/private
@https.route(getPrName, methods=['GET'])
@jwt_required()
@device_ownership_required
def GetPrKeyMain(user_id, device_id):
    return GetPrivateKeyFromID(device_id), 200

# need to add verification if the device belongs to user with jwt token
# curl -X GET http://yourdomain:5000/users/1234/devices/5678/public    
@https.route(getPuName, methods=['GET'])
@jwt_required()
@device_ownership_required
def GetPuKeyMain(user_id, device_id):
    publicKey = GetPublicKeyFromID(device_id)
    if publicKey is None:
        return 'No public key found for device with ID: ' + device_id, 404
    else :
        return GetPublicKeyFromID(device_id), 200

# curl -X POST -H "Content-Type: application/json" http://yourdomain:5000/users/1234/devices/5678/sign    
# Verify ownership, sign message with private key in database, hash the message and then return hashed message
@https.route(signingName, methods=['POST'])
@jwt_required()
@device_ownership_required
def SignMessageMain(user_id, device_id):
    data = CheckContentType()
    if(data):
        privateKey = GetPrivateKeyFromID(device_id)
        print('Task succeeded')
        message = SignWithPrivateKey(privateKey, data)
        response = {"signed_message": message}
        return response, 200
    else:
        return 'Task failed', 401
    
# Verify ownership, sign message with private key in database, hash the message and then return hashed message. Split in 62 bytes messages
@https.route(splitSigningName, methods=['POST'])
def SplitSignMessageMain(device_id):
    data = CheckContentType()
    if(data):
        privateKey = GetPrivateKeyFromID(device_id)
        message = SignWithPrivateKey(privateKey, data)
        splitMessage = list(more_itertools.chunked(message.encode(), 62))
        print('Task succeeded')
        return splitMessage, 200
    else:
        return 'Task failed', 401

if __name__ == "__main__":
    https.run(port=5002, host='0.0.0.0')
    