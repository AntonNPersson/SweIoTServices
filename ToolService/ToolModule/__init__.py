# Packages
from flask import (
    render_template, redirect, Flask, request, session,
    jsonify, abort, json
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException

from SIOTC import (
    GetModel, GetTable, executeQuery, GetAllObjectsInModel,
    admin_required, GetSession, CreateTableObject
)
from SIOTC.helperhttps import device_ownership_required

from flask_jwt_extended import (
    create_access_token, get_current_user, JWTManager,
    jwt_required, current_user, decode_token
)

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import datetime
import csv
import io
import os

# Endpoints
deviceName = '/administrator/all/devices/all/tools/manager'
batchName = '/administrator/all/batches/all/tools/manager'
configName = '/administrator/all/configs/all/tools/manager'
customerName = '/administrator/all/customers/all/tools/manager'
firmwareName = '/administrator/all/firmwares/all/tools/manager'
keysName = '/administrator/all/keys/all/tools/manager'
ordersName = '/administrator/all/orders/all/tools/manager'
producersName = '/administrator/all/producers/all/tools/manager'
roleName = '/administrator/all/roles/all/tools/manager'
usersName = '/administrator/all/users/all/tools/manager'
index = '/administrator/tools/index'
loginName = '/administrator/tools/login'
csvName = '/administrator/tools/csv'
insertName = '/administrator/all/<object>/all/tools/insert'
removeName = '/administrator/all/<object>/all/tools/remove'

# Configuration
permanenceExpireTime = datetime.timedelta(minutes=365)
cookieSameSite = 'Lax'
cookieSecure = True
cookieHttpOnly = True
sqlAlchemyTrackModifications = False

# dir_path = '/home/ubuntu/config/'
# filename = 'jwt'
file_path = None #os.path.join(dir_path, filename)