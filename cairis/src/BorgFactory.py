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

from Borg import Borg
import os
import DatabaseProxyFactory
from string import strip

def initialise():
  b = Borg()
  cairisRoot = '/usr/local/cairis'

  cfgFileName = ''
  try:
    cfgFileName = os.environ['CAIRIS_CFG']
  except KeyError:
    cfgFileName = 'config/cairis.cnf'    

  cfgFile = open('config/cairis.cnf')
  for cfgLine in cfgFile.readlines():
    cfgTuple = cfgLine.split('=')
    cfgKey = strip(cfgTuple[0])
    cfgVal = strip(cfgTuple[1])
 
    if cfgKey == 'dbhost':
      b.dbHost = cfgVal
    elif cfgKey == 'dbport':
      b.dbPort = int(cfgVal)
    elif cfgKey == 'dbuser':
      b.dbUser = cfgVal
    elif cfgKey == 'dbpasswd':
      b.dbPasswd = cfgVal
    elif cfgKey == 'dbname':
      b.dbName = cfgVal
    elif cfgKey == 'tmp_dir': 
      b.tmpDir = cfgVal
    elif cfgKey == 'root': 
      b.cairisRoot = cfgVal
  cfgFile.close()

  b.dbProxy = DatabaseProxyFactory.build()

  pSettings = b.dbProxy.getProjectSettings()
  b.fontSize = pSettings['Font Size']
  b.apFontSize = pSettings['AP Font Size']
  b.fontName = pSettings['Font Name']

  b.imageDir = b.cairisRoot + '/src/images'
  b.configDir = b.cairisRoot + '/src/config'

  b.mainFrame = None
