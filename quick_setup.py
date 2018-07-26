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
import npyscreen as np
import os
import sys
import MySQLdb
import _mysql_exceptions
from cairis.core.MySQLDatabaseProxy import createDatabaseAccount, createDatabaseAndPrivileges, createDatabaseSchema

__author__ = 'Shamal Faily'

class CAIRISDatabaseConfigurationForm(np.ActionForm):

  def create(self):
    self.findRootDir()
    self.pathName = os.path.realpath(__file__)
    self.pathName = self.pathName.replace("quick_setup.py", "")
    self.name = "Configure CAIRIS database and initial account"
    self.theHost = self.add(np.TitleText, name = "Database host:", value = "localhost")
    self.thePort = self.add(np.TitleText, name = "Database port:", value = "3306")
    self.theRootPassword = self.add(np.TitlePassword, name = "Database root password:", value = "")
    self.theTmpDir = self.add(np.TitleText, name = "Temp directory:", value = "/tmp")
    self.theRootDir = self.add(np.TitleText, name = "Root directory:", value = self.pathName + "cairis")
    self.theImageDir = self.add(np.TitleText, name = "Default image directory:", value = ".")
    self.theFileName = self.add(np.TitleText, name = "CAIRIS configuration file name:", value = os.environ.get("HOME") + "/cairis.cnf")
    self.theWebPort = self.add(np.TitleText,name = "Web port:", value = "7071")
    self.theLogLevel = self.add(np.TitleText,name = "Log level:", value = "warning");
    self.theStaticDir = self.add(np.TitleText,name = "Static directory:", value = self.pathName + "cairis/web")
    self.theUploadDir = self.add(np.TitleText,name = "Upload directory:", value = "/tmp")

    self.theUsername = self.add(np.TitleText, name = "Initial Username:", value = "")
    self.thePassword = self.add(np.TitlePassword, name = "Initial Password:", value = "")

    self.theSecretKey = os.urandom(16).encode('hex')
    self.theSalt = os.urandom(16).encode('hex')

  def findRootDir(self):
    self.defaultRootDir = "/usr/local/lib/python2.7/dist-packages/cairis"
    for cpath in sys.path:
      if "/dist-packages/cairis-" in cpath and cpath.endswith(".egg"):
        self.defaultRootDir = os.path.join(cpath, "cairis")
        break

  def on_ok(self):
    try:
      if (len(self.theUsername.value) > 255):
        raise ARMException("Username cannot be longer than 255 characters")
      if (self.theUsername.value == "root"):
        raise ARMException("Username cannot be root")
      self.createUserDatabase()
      self.createCairisCnf()
      os.environ["CAIRIS_CFG"] = str(self.theFileName.value)
      sys.path.insert(0, self.pathName)
      fileName = os.environ.get("HOME") + "/.bashrc"
      f = open(fileName,'a')
      f.write("export CAIRIS_CFG="+str(self.theFileName.value)+"\n")
      f.write("export PYTHONPATH=${PYTHONPATH}:"+self.pathName+"\n")
      f.close()

      from cairis.bin.add_cairis_user import user_datastore, db
      db.create_all()
      user_datastore.create_user(email=self.theUsername.value, password=self.thePassword.value)
      db.session.commit()
      createDatabaseAccount(self.theRootPassword.value,self.theHost.value,self.thePort.value,self.theUsername.value,'')
      createDatabaseAndPrivileges(self.theRootPassword.value,self.theHost.value,self.thePort.value,self.theUsername.value,'',self.theUsername.value + '_default')
      createDatabaseSchema(self.theRootDir.value,self.theHost.value,self.thePort.value,self.theUsername.value,'',self.theUsername.value + '_default')

      self.parentApp.setNextForm(None)
    except ARMException as e:
      np.notify_confirm(str(e), title = 'Error')
    except SQLAlchemyError as e:
      np.notify_confirm('Error adding CAIRIS user: ' + str(e), title = 'Error')

  def on_cancel(self):
    self.parentApp.setNextForm(None)

  def createUserDatabase(self):
    try:
      rootConn = MySQLdb.connect(host=self.theHost.value,port=int(self.thePort.value),user='root',passwd=self.theRootPassword.value)
      rootCursor = rootConn.cursor()
    except _mysql_exceptions.DatabaseError as e:
      id,msg = e
      exceptionText = 'Error connecting to MySQL (id:' + str(id) + ',message:' + msg + ')'
      raise ARMException(exceptionText)

    try:
      dropUserDbSql = "drop database if exists cairis_user"
      rootCursor.execute(dropUserDbSql)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error removing existing cairis_user database (id: ' + str(id) + ', message: ' + msg
      raise ARMException(exceptionText)

    createDatabaseAccount(self.theRootPassword.value,self.theHost.value,self.thePort.value,'cairis_test','cairis_test')
    createDatabaseAndPrivileges(self.theRootPassword.value,self.theHost.value,self.thePort.value,'cairis_test','cairis_test','cairis_test_default')
    createDatabaseSchema(self.theRootDir.value,self.theHost.value,self.thePort.value,'cairis_test','cairis_test','cairis_test_default')

    try:
      createUserDbSql = "create database if not exists cairis_user"
      rootCursor.execute(createUserDbSql)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error creating cairis_user database (id: ' + str(id) + ', message: ' + msg
      raise ARMException(exceptionText)

    try:
      recursionDepthSql = "set global max_sp_recursion_depth = 255"
      rootCursor.execute(recursionDepthSql)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error setting recursion depth ' + self.theUser.value + ' for ' + self.theDbName.value + ' database (id: ' + str(id) + ', message: ' + msg
      raise ARMException(exceptionText)

    try:
      flushPrivilegesSql = "flush privileges"
      rootCursor.execute(flushPrivilegesSql)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error flushing privileges (id: ' + str(id) + ', message: ' + msg
      raise ARMException(exceptionText)

    rootCursor.close()
    rootConn.close()

  def createCairisCnf(self):
    f = open(self.theFileName.value,'w')
    f.write("rpasswd = " +self.theRootPassword.value + "\n")
    f.write("dbhost = " + self.theHost.value + "\n")
    f.write("dbport = " + self.thePort.value + "\n")
    f.write("tmp_dir = " + self.theTmpDir.value + "\n")
    f.write("root = " + self.theRootDir.value + "\n")
    f.write("default_image_dir = " + self.theImageDir.value + "\n")
    f.write("web_port = " + self.theWebPort.value + "\n")
    f.write("log_level = " + self.theLogLevel.value + "\n")
    f.write("web_static_dir = " + self.theStaticDir.value + "\n")
    f.write("upload_dir = " + self.theUploadDir.value + "\n")

    f.write("\n")
    f.write("secret_key = " + self.theSecretKey + "\n")
    f.write("password_hash = sha512_crypt\n")
    f.write("password_salt = " + self.theSalt + "\n")

    f.close()
    self.parentApp.setNextForm(None)


	
class CAIRISConfigurationApp(np.NPSAppManaged):
  def onStart(self):
    self.addForm("MAIN",CAIRISDatabaseConfigurationForm)


def main(args=None):
  if args is None:
    args = sys.argv[1:]
    App = CAIRISConfigurationApp()
    try:
      App.run()
    except np.wgwidget.NotEnoughSpaceForWidget:
      print "The terminal window is too small to display the configuration form, please resize it and try again."

if __name__ == '__main__':
  main()
