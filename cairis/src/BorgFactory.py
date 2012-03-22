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

DBHOST = "127.0.0.1"
DBPORT = 3306
DBUSER = "irisuser"
DBPASSWD = ""
DBNAME = "arm"

from Borg import Borg
import os
import DatabaseProxyFactory

def initialise():
  b = Borg()
  b.dbHost = DBHOST
  b.dbPort = DBPORT
  b.dbUser = DBUSER
  b.dbPasswd = DBPASSWD
  b.dbName = DBNAME
  b.dbProxy = DatabaseProxyFactory.build()

  pSettings = b.dbProxy.getProjectSettings()
  b.fontSize = pSettings['Font Size']
  b.apFontSize = pSettings['AP Font Size']
  b.fontName = pSettings['Font Name']

  b.mainFrame = None
