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

import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_cors import CORS
import cairis.core.BorgFactory
from cairis.core.Borg import Borg
from cairis.core.dba import dbtoken, accounts,canonicalDbUser,createDbOwnerDatabase,createCairisUserDatabase,createDatabaseAccount,createDatabaseAndPrivileges,createDatabaseSchema,createDefaults,dropUser,databases,dbUsers,dropCairisUserDatabase,isOwner,grantDatabaseAccess,revokeDatabaseAccess,resetUsers,existingAccount
import sys
from random import choice
import string

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
  name = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
  confirmed_at = db.Column(db.DateTime())
  roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db,User, Role)
security = Security(app, user_datastore)

class DBATest(unittest.TestCase):

  def setUp(self):
    pass

  def testCreateShareResetDelete(self):
    b = Borg()
    dropCairisUserDatabase(b.rPasswd,b.dbHost,b.dbPort)
    testAccount = 'dbatest@cairis.org'

    createDbOwnerDatabase(b.rPasswd,b.dbHost,b.dbPort)
    createCairisUserDatabase(b.rPasswd,b.dbHost,b.dbPort)
    with app.app_context():
      db.create_all()
    dropUser(b.rPasswd,b.dbHost,b.dbPort,testAccount)

    accountList = accounts(b.rPasswd,b.dbHost,b.dbPort)
    self.assertEqual(testAccount not in accountList,True)
    rp = ''.join(choice(string.ascii_letters + string.digits) for i in range(255))
    dbAccount = canonicalDbUser(testAccount)
    createDatabaseAccount(b.rPasswd,b.dbHost,b.dbPort,testAccount,dbAccount,rp)
    createDatabaseAndPrivileges(b.rPasswd,b.dbHost,b.dbPort,testAccount,rp,canonicalDbUser(testAccount) + '_default')
    createDatabaseSchema(b.cairisRoot,b.dbHost,b.dbPort,testAccount,rp,dbAccount + '_default')

    with app.app_context():
      user_datastore.create_user(email=testAccount, account=dbAccount, password='test',name = 'Test user')
      db.session.commit()

    self.assertEqual(rp, dbtoken(b.rPasswd,b.dbHost,b.dbPort,testAccount))

    createDefaults(b.cairisRoot,b.dbHost,b.dbPort,testAccount,rp,dbAccount + '_default')
    accountList = accounts(b.rPasswd,b.dbHost,b.dbPort)
    self.assertEqual(testAccount in accountList,True)
    self.assertEqual(existingAccount(testAccount),True)
    self.assertEqual(len(databases(dbAccount)),1)

    createDatabaseAndPrivileges(b.rPasswd,b.dbHost,b.dbPort,dbAccount,rp,canonicalDbUser(testAccount) + '_Test1')
    createDatabaseSchema(b.cairisRoot,b.dbHost,b.dbPort,testAccount,rp,dbAccount + '_Test1')

    self.assertEqual(len(databases(dbAccount)),2)
    self.assertEqual(len(dbUsers(dbAccount + '_Test1')),0)
    self.assertEqual(isOwner(dbAccount,'Test1'),True)

    
    testAccount2 = 'dbatest2@cairis.org'
    rp2 = ''.join(choice(string.ascii_letters + string.digits) for i in range(255))
    dbAccount2 = canonicalDbUser(testAccount2)
    createDatabaseAccount(b.rPasswd,b.dbHost,b.dbPort,testAccount2,dbAccount2,rp2)
    createDatabaseAndPrivileges(b.rPasswd,b.dbHost,b.dbPort,dbAccount2,rp2,canonicalDbUser(testAccount2) + '_default')
    createDatabaseSchema(b.cairisRoot,b.dbHost,b.dbPort,testAccount,rp2,dbAccount2 + '_default')

    with app.app_context():
      user_datastore.create_user(email=testAccount2, account=dbAccount2, password='test',name = 'Test user 2')
      db.session.commit()

    accountList = accounts(b.rPasswd,b.dbHost,b.dbPort)
    self.assertEqual(testAccount2 in accountList,True)
    self.assertEqual(len(databases(dbAccount2)),1)

    grantDatabaseAccess(b.rPasswd,b.dbHost,b.dbPort,'Test1',testAccount2)
    self.assertEqual(len(databases(dbAccount2)),2)
    self.assertEqual(len(dbUsers(dbAccount + '_Test1')),1)
    self.assertEqual(isOwner(dbAccount2,'Test1'),False)

    revokeDatabaseAccess(b.rPasswd,b.dbHost,b.dbPort,'Test1',testAccount2)
    self.assertEqual(len(databases(dbAccount2)),1)
    self.assertEqual(len(dbUsers(dbAccount + '_Test1')),0)

    resetUsers(b.cairisRoot,b.rPasswd,b.dbHost,b.dbPort)
    self.assertEqual(len(databases(dbAccount)),1)
    self.assertEqual(len(databases(dbAccount2)),1)

    dropUser(b.rPasswd,b.dbHost,b.dbPort,testAccount)
    dropUser(b.rPasswd,b.dbHost,b.dbPort,testAccount2)
    accountList = accounts(b.rPasswd,b.dbHost,b.dbPort)
    self.assertEqual(testAccount not in accountList,True)
    self.assertEqual(testAccount2 not in accountList,True)
  
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
