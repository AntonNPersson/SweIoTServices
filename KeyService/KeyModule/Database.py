from KeyModule import GetKeys, executeQuery, Devices
from .crypto import HashToPem, PemToHash
import json

def GetPrivateKeyFromID(id):
    def queryFunc(session, base, id):
        # Query the database for the private key associated with the provided ID
        Key = session.query(GetKeys(base)).filter_by(device_id=id).first()
        if Key is None:
            return None, 'No key found with device ID: ' + id
        print('Success')
        # Return the private key
        return Key.privatekey
    return executeQuery(queryFunc, id)
    
def GetPublicKeyFromID(id):
    def queryFunc(session, base, id):
        try:
            # Query the keys table to get the key with the specified device_id
            Key = session.query(GetKeys(base)).filter_by(device_id=id).first()
            # Raise an exception if no key is found
            if Key is None:
                return None, 'No key found with device ID: ' + id
            print('Success')
            # Return the public key as a PEM-encoded string
            private_key = HashToPem(Key.privatekey, 'RSA Private Key')
            response = {"private_key": private_key}
            return json.dumps(response)
        except Exception:
            return None, 404
    return executeQuery(queryFunc, id)

def RemoveKeyPairFromDevice(deviceId):
    def queryFunc(session, base, deviceId):
        try:
            # Query the keys table to get the key with the specified device_id
            Key = session.query(GetKeys(base)).filter_by(device_id=deviceId).first()
            # Raise an exception if no key is found
            if Key is None:
                return None, 'No key found with device ID: ' + deviceId
            # Delete the key from the database
            session.delete(Key)
            session.commit()
            print('Key deleted successfully')
            return 'Key deleted successfully'
        except Exception:
            return 'An error occurred while deleting the key'
    return executeQuery(queryFunc, deviceId)

def RemoveMultipleKeyPairFromDevice(deviceIds):
    def queryFunc(session, base, deviceIds):
        try:
            # Query the keys table to get the key with the specified device_id
            for deviceId in deviceIds:
                Key = session.query(GetKeys(base)).filter_by(device_id=deviceId).first()
                # Raise an exception if no key is found
                if Key is None:
                    return None, 'No key found with device ID: ' + deviceId
                # Delete the key from the database
                session.delete(Key)
            session.commit()
            print('Key deleted successfully')
            return 'Key deleted successfully'
        except Exception:
            return 'An error occurred while deleting the key'
    return executeQuery(queryFunc, deviceIds)

def AddKeyPairFromDevice(privateKey, publicKey, deviceId):
    def queryFunc(session, base, privateKey, publicKey, deviceId):
        try:
            # Validate inputs
            if not privateKey:
                return "Private key is empty"
            if not publicKey:
                return "Public key is empty"
            if not deviceId:
                return "Device ID is empty"

            # Find customerid from deviceid (temporary until auth working)
            device = session.query(Devices(base)).filter_by(id=deviceId).first()
            if not device:
                return "No device found with device ID: " + deviceId
            customerId = device.customer_id

            # Insert keys into database
            keysTable = base.metadata.tables.get('public.rsakeys')
            existingKey = session.query(keysTable).filter_by(device_id=deviceId).first()
            if existingKey:
                return "Key pair already exists for device with ID: " + deviceId

            newKeys = keysTable.insert().values(privatekey=privateKey, publickey=publicKey, device_id=deviceId,
                                                customer_id=customerId)
            session.execute(newKeys)
            session.commit()
            print('Key pair added successfully')
            return 'Key pair added successfully'
        except Exception:
            return 'An error occurred while adding the key pair'
    return executeQuery(queryFunc, privateKey, publicKey, deviceId)


def AddKeyPairFromMac(privateKey, publicKey, mac):
    def queryFunc(session, base, privateKey, publicKey, mac):
        # Hash key values
        hashedPrK = PemToHash(privateKey)
        hashedPuB = PemToHash(publicKey)
        # Look up device ID and customer ID from database using MAC address
        device = session.query(Devices(base)).filter_by(mac_adress=mac).first()
        if not device:
            raise ValueError("No device found with MAC address " + mac)
        deviceId = device.id
        customerId = device.customer_id
        # Create table object and insert new keys
        keysTable = base.metadata.tables.get('public.rsakeys')
        existingKey = session.query(keysTable).filter_by(device_id=deviceId).first()
        if existingKey:
            raise ValueError("Key pair already exist for device with ID: " + deviceId)
        newKeys = keysTable.insert().values(privatekey=hashedPrK, publickey=hashedPuB, device_id=deviceId, customer_id=customerId)
        session.execute(newKeys)
        session.commit()
        print('success')
        return 'Success'
    return executeQuery(queryFunc, privateKey, publicKey, mac)
    
def GetPrivateKeyFromMAC(mac):
    def queryFunc(session, base, mac):
       # Query the database to get the device object by its MAC address
        device = session.query(Devices(base)).filter_by(mac_adress=mac).first()
        # Query the database to get the key object associated with the device
        Key = session.query(GetKeys(base)).filter_by(device_id=device.id).first()
        # Convert the private key to a PEM format
        pem_key = HashToPem(Key.privatekey, 'RSA Private Key')
        # Return the PEM formatted private key
        print('Success')
        return pem_key
    return executeQuery(queryFunc, mac)