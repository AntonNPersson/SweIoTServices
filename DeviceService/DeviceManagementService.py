import sqlalchemy
from DeviceModule import ownsDeviceName, GetFromTable, jsonify, get_jwt_identity, jwt_required, JWTManager, Flask, lookUpAllName, GetAllObjectsInModel, GetSpecificFromColumnInTable
import os, logging

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = '3'
logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

@jwt_required()
@app.route(lookUpAllName, methods=['GET'])
def lookUp(user_id):
    userid = get_jwt_identity()
    if userid != user_id:
        return 'Currently logged in to user: ' + userid + ' and not user: ' + user_id, 401
    customer = GetSpecificFromColumnInTable(userid, 'customer_id', 'users')
    if customer is None:
        return 'No customer found', 404
    deviceModels = GetAllObjectsInModel('devices').filter_by(customer_id=customer).all()
    devicesMac = []
    devicesID = []
    for device in deviceModels:
        devicesMac.append(device.__dict__['mac_adress'])
        devicesID.append(device.__dict__['id'])
    return jsonify({'Mac': devicesMac, 'ID': devicesID}), 200

@jwt_required()
@app.route(ownsDeviceName, methods=['GET'])
def ownsDevice(user_id, device_id):
    userid = get_jwt_identity()
    if userid != user_id:
        return 'Currently logged in to user: ' + userid + ' and not user: ' + user_id, 401
    customer = GetSpecificFromColumnInTable(user_id, 'customer_id', 'users')
    if customer is None:
        return 'No customer found', 404
    device = GetFromTable('devices', device_id)
    if device is None:
        return 'No device found', 404
    if device.__dict__['customer_id'] != customer:
        return False, 401
    return True, 200


if __name__ == '__main__':
    app.run(port=5003, host='0.0.0.0')
