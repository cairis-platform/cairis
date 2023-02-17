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

from cairis.core.ARM import ARMException
from sqlalchemy.exc import SQLAlchemyError
import os
import sys
from cairis.core.dba import createDatabaseAccount, createDbOwnerDatabase, createDatabaseAndPrivileges, createDatabaseSchema, createDefaults, canonicalDbUser, dropCairisUserDatabase, createCairisUserDatabase
from flask_security import hash_password
import binascii
from random import choice
from string import ascii_letters, digits
from subprocess import Popen
from shlex import split


__author__ = 'Shamal Faily'


def quick_setup(dbHost,dbPort,dbRootPassword,tmpDir,rootDir,configFile,webPort,logLevel,staticDir,assetDir,userName,passWd,mailServer = '',mailPort = '',mailUser = '',mailPasswd = ''):
  if (len(userName) > 255):
    raise ARMException("Username cannot be longer than 255 characters")
  if (userName == "root"):
    raise ARMException("Username cannot be root")
  createCairisCnf(configFile,dbRootPassword,dbHost,dbPort,tmpDir,rootDir,webPort,logLevel,staticDir,assetDir,mailServer,mailPort,mailUser,mailPasswd)
  os.environ["CAIRIS_CFG"] = configFile
  createDbOwnerDatabase(dbRootPassword,dbHost,dbPort)
  createUserDatabase(dbHost,dbPort,dbRootPassword,rootDir)
  pathName = os.path.split(os.path.split(os.path.realpath(os.path.dirname(__file__)))[0])[0]
  sys.path.insert(0, pathName)
  fileName = os.environ.get("HOME") + "/.bashrc"
  f = open(fileName,'a')
  f.write("export CAIRIS_SRC="+ rootDir + "\n")
  f.write("export CAIRIS_CFG_DIR=${CAIRIS_SRC}/config\n")
  f.write("export CAIRIS_CFG="+ configFile +"\n")
  f.write("export PYTHONPATH=${PYTHONPATH}:" + pathName +"\n")
  f.close()

  from cairis.bin.add_cairis_user import user_datastore,db
  db.create_all()

  if (userName != ''):
    rp = ''.join(choice(ascii_letters + digits) for i in range(255))
    dbAccount = canonicalDbUser(userName)
    user_datastore.create_user(email=userName, account=dbAccount, password=hash_password(passWd),name = 'Default user')
    db.session.commit()
    createDatabaseAccount(dbRootPassword,dbHost,dbPort,userName,dbAccount,rp)
    createDatabaseAndPrivileges(dbRootPassword,dbHost,dbPort,userName,rp,dbAccount + '_default')
    createDatabaseSchema(rootDir,dbHost,dbPort,userName,rp,dbAccount + '_default')
    createDefaults(rootDir,dbHost,dbPort,userName,rp,dbAccount + '_default')


def createUserDatabase(dbHost,dbPort,dbRootPassword,rootDir):
  dropCairisUserDatabase(dbRootPassword,dbHost,dbPort)
  createCairisUserDatabase(dbRootPassword,dbHost,dbPort)
  createDatabaseAccount(dbRootPassword,dbHost,dbPort,'cairis_test','cairis_test','cairis_test')
  createDatabaseAndPrivileges(dbRootPassword,dbHost,dbPort,'cairis_test','cairis_test','cairis_test_default')
  createDatabaseSchema(rootDir,dbHost,dbPort,'cairis_test','cairis_test','cairis_test_default')


def createCairisCnf(configFile,dbRootPassword,dbHost,dbPort,tmpDir,rootDir,webPort,logLevel,staticDir,assetDir,mailServer,mailPort,mailUser,mailPasswd):
  f = open(configFile,'w')
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
  f.close()
