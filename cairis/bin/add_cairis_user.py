#!/usr/bin/python3
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

import argparse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_cors import CORS
from cairis.core.Borg import Borg
from cairis.core.dba import createDatabaseAccount,createDatabaseAndPrivileges,createDatabaseSchema, createDefaults, canonicalDbUser, existingAccount
import cairis.core.BorgFactory
from random import choice
import string
import sys

__author__ = 'Shamal Faily'

cairis.core.BorgFactory.dInitialise()
app = Flask(__name__)
app.config['DEBUG'] = True
b = Borg()
app.config['SECRET_KEY'] = b.secretKey
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:' + b.rPasswd + '@' + b.dbHost + '/cairis_user'

db = SQLAlchemy(app)
cors = CORS(app)

roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('auth_user.id')), db.Column('role_id', db.Integer(), db.ForeignKey('auth_role.id')))

class Role(db.Model, RoleMixin):
  __tablename__ = 'auth_role'
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(80), unique=True)
  description = db.Column(db.String(255))

class User(db.Model, UserMixin):
  __tablename__ = 'auth_user'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  account = db.Column(db.String(32), unique=True)
  password = db.Column(db.String(255))
  dbtoken = db.Column(db.String(255))
  name = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db,User, Role)
security = Security(app, user_datastore)

def addAdditionalUserData(userName,passWd):
  fUser = user_datastore.get_user(userName)
  rp = ''.join(choice(string.ascii_letters + string.digits) for i in range(255))
  fUser.dbtoken = rp
  db.session.commit()
  b = Borg()
  dbAccount = canonicalDbUser(userName)
  createDatabaseAccount(b.rPasswd,b.dbHost,b.dbPort,userName,rp)
  createDatabaseAndPrivileges(b.rPasswd,b.dbHost,b.dbPort,userName,rp,dbAccount + '_default')
  createDatabaseSchema(b.cairisRoot,b.dbHost,b.dbPort,userName,rp,dbAccount + '_default')
  createDefaults(b.cairisRoot,b.dbHost,b.dbPort,userName,rp,dbAccount + '_default')
  

def main():
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Add CAIRIS user')
  parser.add_argument('user',help='Email address')
  parser.add_argument('password',help='password')
  parser.add_argument('name',help='Full name')
  args = parser.parse_args()

  rp = ''.join(choice(string.ascii_letters + string.digits) for i in range(255))

  if (existingAccount(args.user)):
    raise Exception(args.user + ' already exists')

  dbAccount = canonicalDbUser(args.user)
  createDatabaseAccount(b.rPasswd,b.dbHost,b.dbPort,dbAccount,rp)
  createDatabaseAndPrivileges(b.rPasswd,b.dbHost,b.dbPort,dbAccount,rp,canonicalDbUser(args.user) + '_default')
  createDatabaseSchema(b.cairisRoot,b.dbHost,b.dbPort,args.user,rp,dbAccount + '_default')

  db.create_all()
  user_datastore.create_user(email=args.user, account=dbAccount, password=args.password,dbtoken=rp,name = 'Default user')
  db.session.commit()

  createDefaults(b.cairisRoot,b.dbHost,b.dbPort,args.user,rp,dbAccount + '_default')


if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print('Fatal add_cairis_user error: ' + str(e))
    sys.exit(-1)

