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

import npyscreen as np
import os
import sys
import MySQLdb
import _mysql_exceptions
from subprocess import Popen

__author__ = 'Shamal Faily'

class CAIRISDatabaseConfigurationForm(np.ActionForm):

  def create(self):
    self.findRootDir()
    self.pathName = os.path.realpath(__file__)
    self.pathName = self.pathName.replace("quick_setup.py", "")
    self.name = "Configure CAIRIS Database"
    self.theHost = self.add(np.TitleText, name = "Database host:", value = "localhost")
    self.thePort = self.add(np.TitleText, name = "Database port:", value = "3306")
    self.theRootPassword = self.add(np.TitlePassword, name = "Database root password:", value = "")
    self.theDbName = self.add(np.TitleText, name = "Database name (created if non-existent):", value = "cairis")
    self.theUser = self.add(np.TitleText, name = "Database user (created if non-existent):", value = "cairisuser")
    defaultUserPassword = os.urandom(10).encode('hex')
    self.thePassword = self.add(np.TitlePassword, name = "Database user password:", value = defaultUserPassword)
    self.theTmpDir = self.add(np.TitleText, name = "Temp directory:", value = "/tmp")
    self.theRootDir = self.add(np.TitleText, name = "Root directory:", value = self.pathName + "cairis")
    self.theImageDir = self.add(np.TitleText, name = "Default image directory:", value = ".")
    self.theFileName = self.add(np.TitleText, name = "CAIRIS configuration file name:", value = os.environ.get("HOME") + "/cairis.cnf")
    self.theWebPort = self.add(np.TitleText,name = "Web port:", value = "7071")
    self.theLogLevel = self.add(np.TitleText,name = "Log level:", value = "warning");
    self.theStaticDir = self.add(np.TitleText,name = "Static directory:", value = self.pathName + "cairis/web")
    self.theUploadDir = self.add(np.TitleText,name = "Upload directory:", value = "/tmp")

    self.theSecretKey = os.urandom(16).encode('hex')
    self.theSalt = os.urandom(16).encode('hex')

  def findRootDir(self):
    self.defaultRootDir = "/usr/local/lib/python2.7/dist-packages/cairis"
    for cpath in sys.path:
      if "/dist-packages/cairis-" in cpath and cpath.endswith(".egg"):
        self.defaultRootDir = os.path.join(cpath, "cairis")
        break

  def on_ok(self):
    self.createDatabase()
    self.initialiseDatabase()
    self.createCairisCnf()
    os.environ["CAIRIS_CFG"] = str(self.theFileName.value)
    sys.path.insert(0, self.pathName)
    fileName = os.environ.get("HOME") + "/.bashrc"
    f = open(fileName,'a')
    f.write("export CAIRIS_CFG="+str(self.theFileName.value)+"\n")
    f.write("export PYTHONPATH=${PYTHONPATH}:"+self.pathName+"\n")
    f.close()
    self.parentApp.setNextForm("NEXT")

  def on_cancel(self):
    self.parentApp.setNextForm(None)

  def createDatabase(self):
    rootConn = MySQLdb.connect(host=self.theHost.value,port=int(self.thePort.value),user='root',passwd=self.theRootPassword.value)
    rootCursor = rootConn.cursor()

    try:
      grantUsageSql = "grant usage on *.* to '" + self.theUser.value + "'@'" + self.theHost.value + "' identified by '" + self.thePassword.value + "' with max_queries_per_hour 0 max_connections_per_hour 0 max_updates_per_hour 0 max_user_connections 0"
      rootCursor.execute(grantUsageSql)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error granting usage to ' + self.theUser.value + ' (id: ' + str(id) + ', message: ' + msg

    try:
      createSql = "create database if not exists `" + self.theDbName.value + "`"
      rootCursor.execute(createSql)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error creating ' + self.theDbName.value + ' database (id: ' + str(id) + ', message: ' + msg

    try:
      grantPrivilegesSql = "grant all privileges on `" + self.theDbName.value + "`.* to '" + self.theUser.value + "'@'" + self.theHost.value + "'"
      rootCursor.execute(grantPrivilegesSql)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error granting privileges to ' + self.theUser.value + ' for ' + self.theDbName.value + ' database (id: ' + str(id) + ', message: ' + msg

    try:
      recursionDepthSql = "set global max_sp_recursion_depth = 255"
      rootCursor.execute(recursionDepthSql)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error setting recursion depth ' + self.theUser.value + ' for ' + self.theDbName.value + ' database (id: ' + str(id) + ', message: ' + msg

    try:
      flushPrivilegesSql = "flush privileges"
      rootCursor.execute(flushPrivilegesSql)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error flushing privileges (id: ' + str(id) + ', message: ' + msg

    rootCursor.close()
    rootConn.close()

  def initialiseDatabase(self):
    initDbCmd = "mysql --user=" + self.theUser.value + " --password=" + self.thePassword.value + " --database=" + self.theDbName.value + " < " + self.theRootDir.value + "/sql/init.sql"
    p = Popen(initDbCmd,shell=True)
    os.waitpid(p.pid,0)

    procsCmd = "mysql --user=" + self.theUser.value + " --password=" + self.thePassword.value + " --database=" + self.theDbName.value + " < " + self.theRootDir.value + "/sql/procs.sql"
    p = Popen(procsCmd,shell=True)
    os.waitpid(p.pid,0)


  def createCairisCnf(self):
    f = open(self.theFileName.value,'w')
    f.write("dbhost = " + self.theHost.value + "\n")
    f.write("dbport = " + self.thePort.value + "\n")
    f.write("dbuser = " + self.theUser.value + "\n")
    f.write("dbpasswd = " + self.thePassword.value + "\n")
    f.write("dbname = " + self.theDbName.value + "\n")
    f.write("tmp_dir = " + self.theTmpDir.value + "\n")
    f.write("root = " + self.theRootDir.value + "\n")
    f.write("default_image_dir = " + self.theImageDir.value + "\n")
    f.write("web_port = " + self.theWebPort.value + "\n")
    f.write("log_level = " + self.theLogLevel.value + "\n")
    f.write("web_static_dir = " + self.theStaticDir.value + "\n")
    f.write("upload_dir = " + self.theUploadDir.value + "\n")

    f.write("\n")
    f.write("auth_dbhost = " + self.theHost.value + "\n")
    f.write("auth_dbuser = " + self.theUser.value + "\n")
    f.write("auth_dbpasswd = " + self.thePassword.value + "\n")
    f.write("auth_dbname = " + self.theDbName.value + "\n")

    f.write("\n")
    f.write("secret_key = " + self.theSecretKey + "\n")
    f.write("password_hash = sha512_crypt\n")
    f.write("password_salt = " + self.theSalt + "\n")

    f.close()
    self.parentApp.setNextForm(None)

class CAIRISUserConfigurationForm(np.ActionForm):


  def create(self):
    self.name = "Add CAIRIS User"
    self.theUsername = self.add(np.TitleText, name = "Username:", value = "test")
    self.thePassword = self.add(np.TitlePassword, name = "Password:", value = "")

  def on_ok(self):
    from cairis.bin.add_cairis_user import user_datastore, db
    db.create_all()
    user_datastore.create_user(email=self.theUsername.value, password=self.thePassword.value)
    db.session.commit()
    self.parentApp.setNextForm(None)
	
  def on_cancel(self):
    self.parentApp.setNextForm(None)

class CAIRISConfigurationApp(np.NPSAppManaged):
  def onStart(self):
    self.addForm("MAIN",CAIRISDatabaseConfigurationForm)
    self.addForm("NEXT",CAIRISUserConfigurationForm)


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
