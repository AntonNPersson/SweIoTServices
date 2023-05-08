from KeyModule import GetKeys, executeQuery, Devices
from .crypto import HashToPem, PemToHash

def GetPrivateKeyFromID(id):
    def queryFunc(session, base, id):
        # Query the database for the private key associated with the provided ID
        Key = session.query(GetKeys(base)).filter_by(device_id=id).first()
        if(Key is None):
            raise ValueError("No key found with device ID: " + id)
        print('Success')
        # Return the private key
        return Key.privatekey
    return executeQuery(queryFunc, id)
    
def GetPublicKeyFromID(id):
    def queryFunc(session, base, id):
        # Query the keys table to get the key with the specified device_id
        Key = session.query(GetKeys(base)).filter_by(device_id=id).first()
        # Print a success message to indicate that the key was found
        if(Key is None):
            raise ValueError("No key found with device ID: " + id)
        print('Success')
        # Return the public key as a PEM-encoded string
        return HashToPem(Key.publickey, 'RSA Public Key')
    return executeQuery(queryFunc, id)


def AddKeyPairFromDevice(privateKey, publicKey, deviceId):
    def queryFunc(session, base, privateKey, publicKey, deviceId):
        # Validate inputs
        if not privateKey:
            raise ValueError("Private key is empty")
        if not publicKey:
            raise ValueError("Public key is empty")
        if not deviceId:
            raise ValueError("Device ID is empty")
        # Find customerid from devideid (temporary until auth working)
        device = session.query(Devices(base)).filter_by(id=deviceId).first()
        if not device:
            raise ValueError("No device found with device ID: " + deviceId) 
        customerId = device.customer_id
        # Insert keys into database
        keysTable = base.metadata.tables.get('public.rsakeys')
        existingKey = session.query(keysTable).filter_by(device_id=deviceId).first()
        if existingKey:
            raise ValueError("Key pair already exist for device with ID: " + deviceId)
        newKeys = keysTable.insert().values(privatekey=privateKey, publickey=publicKey, device_id=deviceId, customer_id=customerId)
        session.execute(newKeys)
        session.commit()
        print('Key pair added successfully')
        return 'Key pair added successfully'
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