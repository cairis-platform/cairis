#!/usr/bin/env python

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

import binascii
import os
import sys
from random import choice
from string import ascii_letters, digits

from flask_security import hash_password

from cairis.core.ARM import ARMException
from cairis.core.dba import (
  canonicalDbUser,
  createCairisUserDatabase,
  createDatabaseAccount,
  createDatabaseAndPrivileges,
  createDatabaseSchema,
  createDbOwnerDatabase,
  createDefaults,
  dropCairisUserDatabase,
)

__author__ = 'Shamal Faily'

def validate_username(userName: str):
  if userName == "":
    return

  if (userName == "root"):
    raise ARMException("Username cannot be root")

  if (len(userName) > 255):
    raise ARMException("Username cannot be longer than 255 characters")

def inject_bashrc(rootDir: str, configFile: str):
  fileName = os.environ.get("HOME") + "/.bashrc"

  if not os.path.exists(fileName):
    return

  with open(fileName,'a') as f:
    f.write("export CAIRIS_SRC="+ rootDir + "\n")
    f.write("export CAIRIS_CFG_DIR=${CAIRIS_SRC}/config\n")
    f.write("export CAIRIS_CFG="+ configFile +"\n")

    pathName = os.path.split(os.path.split(os.path.realpath(os.path.dirname(__file__)))[0])[0]
    sys.path.insert(0, pathName)

    f.write("export PYTHONPATH=${PYTHONPATH}:" + pathName +"\n")

def quick_setup(dbHost,dbPort,dbRootPassword,tmpDir,rootDir,configFile,webPort,logLevel,staticDir,assetDir,userName,passWd,mailServer = '',mailPort = '',mailUser = '',mailPasswd = ''):
  createCairisCnf(configFile,dbRootPassword,dbHost,dbPort,tmpDir,rootDir,webPort,logLevel,staticDir,assetDir,mailServer,mailPort,mailUser,mailPasswd)

  import MySQLdb
  with MySQLdb.connect(host=dbHost,user='root',passwd=dbRootPassword) as con:
    with con.cursor() as cur:
      if cur.execute('SHOW DATABASES LIKE "cairis_owner"') == 1:
        return

  validate_username(userName)

  createDbOwnerDatabase(dbRootPassword,dbHost,dbPort)
  createUserDatabase(dbHost,dbPort,dbRootPassword,rootDir)

  os.environ["CAIRIS_CFG"] = configFile
  from cairis.bin.add_cairis_user import db
  db.create_all()

  if userName:
    createUser(rootDir, dbRootPassword, dbHost, dbPort, userName, passWd)

  inject_bashrc(rootDir, configFile)

def createUserDatabase(dbHost,dbPort,dbRootPassword,rootDir):
  dropCairisUserDatabase(dbRootPassword,dbHost,dbPort)
  createCairisUserDatabase(dbRootPassword,dbHost,dbPort)
  createDatabaseAccount(dbRootPassword,dbHost,dbPort,'cairis_test','cairis_test','cairis_test')
  createDatabaseAndPrivileges(dbRootPassword,dbHost,dbPort,'cairis_test','cairis_test','cairis_test_default')
  createDatabaseSchema(rootDir,dbHost,dbPort,'cairis_test','cairis_test','cairis_test_default')

def createUser(rootDir,dbRootPassword,dbHost,dbPort,userName,passWd):
  from cairis.bin.add_cairis_user import db, user_datastore

  rp = ''.join(choice(ascii_letters + digits) for i in range(255))
  dbAccount = canonicalDbUser(userName)
  user_datastore.create_user(email=userName, account=dbAccount, password=hash_password(passWd),name = 'Default user')
  db.session.commit()
  createDatabaseAccount(dbRootPassword,dbHost,dbPort,userName,dbAccount,rp)
  createDatabaseAndPrivileges(dbRootPassword,dbHost,dbPort,userName,rp,dbAccount + '_default')
  createDatabaseSchema(rootDir,dbHost,dbPort,userName,rp,dbAccount + '_default')
  createDefaults(rootDir,dbHost,dbPort,userName,rp,dbAccount + '_default')

def createCairisCnf(configFile,dbRootPassword,dbHost,dbPort,tmpDir,rootDir,webPort,logLevel,staticDir,assetDir,mailServer,mailPort,mailUser,mailPasswd):
  with open(configFile,'w') as f:
    f.write("rpasswd = " + dbRootPassword + "\n")
    f.write("dbhost = " + dbHost + "\n")
    f.write("dbport = " + str(dbPort) + "\n")
    f.write("tmp_dir = " + tmpDir + "\n")
    f.write("root = " + rootDir + "\n")
    f.write("web_port = " + str(webPort) + "\n")
    f.write("log_level = " + logLevel + "\n")
    f.write("web_static_dir = " + staticDir + "\n")
    f.write("web_asset_dir = " + assetDir + "\n")
    f.write("mail_server = " + mailServer + "\n")
    f.write("mail_port = " + mailPort + "\n")
    f.write("mail_user = " + mailUser + "\n")
    f.write("mail_passwd = " + mailPasswd + "\n")

    f.write("\n")
    f.write("secret_key = " + str(binascii.hexlify(os.urandom(16))) + "\n")
