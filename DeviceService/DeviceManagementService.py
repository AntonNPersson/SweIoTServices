import sqlalchemy
from DeviceModule.Database import GetIdFromMac, is_mac_address
from DeviceModule import ownsDeviceName, GetFromTable, jsonify, get_jwt_identity, jwt_required, JWTManager, Flask, lookUpAllName, GetAllObjectsInModel, GetSpecificFromColumnInTable
import os, logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

dir_path = '/home/ubuntu/config/'
filename = 'jwt'
file_path = os.path.join(dir_path, filename)

with open(file_path, 'r') as f:
    # Write the connection string to the file
    first_line = f.readline()

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = first_line
logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

@app.route(lookUpAllName, methods=['GET'])
@jwt_required()
def lookUp(user_id):
    try:
        userid = get_jwt_identity()
        if userid != user_id:
            return 'Currently logged in to user: ' + userid + ' and not user: ' + user_id, 401
        customer = GetSpecificFromColumnInTable(userid, 'customer_id', 'users')
        if customer is None:
            return 'No customer found', 200
        deviceModels = GetAllObjectsInModel('devices').filter_by(customer_id=customer).all()
        devicesMac = []
        devicesID = []
        for device in deviceModels:
            devicesMac.append(device.__dict__['mac_adress'])
            devicesID.append(device.__dict__['id'])
        return jsonify({'Mac': devicesMac, 'ID': devicesID}), 200
    except (SQLAlchemyError, IntegrityError, ValueError, TypeError) as e:
        app.logger.error(e)
        return 'Error: Check Logs', 500

@app.route(ownsDeviceName, methods=['GET'])
@jwt_required()
def ownsDevice(user_id, device_id):
    try:
        userid = get_jwt_identity()
        customer = GetSpecificFromColumnInTable(userid, 'customer_id', 'users')
        if customer is None:
            return str(False), 200
        if is_mac_address(device_id):
            device_id = GetIdFromMac(device_id)
        device = GetSpecificFromColumnInTable(device_id, 'customer_id', 'devices')
        if device is None or device != customer:
            return str(False), 200
        return str(True), 200
    except (SQLAlchemyError, IntegrityError, ValueError, TypeError) as e:
        app.logger.error(e)
        return 'Error: Check Logs', 500


if __name__ == '__main__':
    app.run(port=5003, host='0.0.0.0')
