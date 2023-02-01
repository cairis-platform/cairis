#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

__author__ = 'Robin Quetin, Shamal Faily'

import logging
import os
import sys
if (sys.version_info > (3,)):
  import http.client
else:
  import httplib
from flask import Flask
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore, user_registered
from flask_security import Security, SQLAlchemyUserDatastore
from cairis.bin.add_cairis_user import addAdditionalUserData
from flask_cors import CORS
from cairis.core.Borg import Borg
from cairis.daemon.WebConfig import *
from .cdb import db
from .models import User, Role

app = Flask(__name__)

@user_registered.connect_via(app)
def enroll(sender, user, confirm_token,confirmation_token=None,form_data = {}):
  addAdditionalUserData(user.email, user.password)


def create_app():
  options = {
    'port' : 0,
    'unitTesting': False
  }
  WebConfig.config(options)

  b = Borg()
  app.config['DEBUG'] = True
  app.config['SECRET_KEY'] = b.secretKey
  app.config['SECURITY_PASSWORD_SALT'] = 'None'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:' + b.rPasswd + '@' + b.dbHost + '/cairis_user'

  if (b.mailServer != '' and b.mailPort != '' and b.mailUser != '' and b.mailPasswd != ''):
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_RECOVERABLE'] = True
    app.config['MAIL_SERVER'] = b.mailServer
    app.config['MAIL_PORT'] = b.mailPort
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = b.mailUser
    app.config['MAIL_PASSWORD'] = b.mailPasswd
    app.config['SECURITY_EMAIL_SENDER'] = b.mailUser

  b.logger.setLevel(b.logLevel)
  b.logger.debug('Error handlers: {0}'.format(app.error_handler_spec))
  app.secret_key = os.urandom(24)
  logger = logging.getLogger('werkzeug')
  logger.setLevel(b.logLevel)
  enable_debug = b.logLevel = logging.DEBUG

  mail = Mail(app)
  cors = CORS(app)
  with app.app_context():
    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db,User, Role)
    security = Security(app, user_datastore)

    from .main import main as main_blueprint 
    app.register_blueprint(main_blueprint)
    db.create_all()
  return app

def create_test_app():
  options = {
    'port' : 0,
    'unitTesting': True
  }
  WebConfig.config(options)

  b = Borg()
  app = Flask(__name__)
  app.config['DEBUG'] = True
  app.config['SECRET_KEY'] = b.secretKey
  app.config['SECURITY_PASSWORD_SALT'] = 'None'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:' + b.rPasswd + '@' + b.dbHost + '/cairis_user'
  b.logger.setLevel(b.logLevel)
  b.logger.debug('Error handlers: {0}'.format(app.error_handler_spec))
  app.secret_key = os.urandom(24)
  logger = logging.getLogger('werkzeug')
  logger.setLevel(b.logLevel)
  enable_debug = b.logLevel = logging.DEBUG
  db.init_app(app)
  user_datastore = SQLAlchemyUserDatastore(db,User, Role)
  security = Security(app, user_datastore)
  from .main import main as main_blueprint 
  app.register_blueprint(main_blueprint)
  with app.app_context():
    db.create_all()
  return app
