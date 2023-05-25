from DeviceModule import executeQuery, GetModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import re

def GetIdFromMac(mac):
    def queryFunc(session, base, mac):
        # Query the database for the device with the provided mac address
        device = session.query(GetModel('devices', session, base)).filter_by(mac_adress=mac).first()
        # Check if an error occurred during retrieval
        if device is None:
            print('Error: No device exist with provided mac address')
            return None
        # If no error, return the device's id
        else:
            return device.id
    return executeQuery(queryFunc, mac)

def GetIdFromMacWithoutSession(mac, session, base):
    # Query the database for the device with the provided mac address
    device = session.query(GetModel('devices')).filter_by(mac_adress=mac).first()
    # Check if an error occurred during retrieval
    if device is None:
        print('Error: No device exist with provided mac address')
        return None
    # If no error, return the device's id
    else:
        return device.id

def is_mac_address(string):
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return re.match(pattern, string) is not None