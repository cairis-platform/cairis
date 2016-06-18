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
import logging
import DatabaseProxyFactory
from cairis.tools.GraphicsGenerator import GraphicsGenerator
from MySQLDatabaseProxy import MySQLDatabaseProxy
from TemplateGenerator import TemplateGenerator
from ARM import ARMException
from string import strip

def parseConfigFile():
  b = Borg()
  cfgFileName = ''
  try:
    cfgFileName = os.environ['CAIRIS_CFG']
  except KeyError:
    raise ARMException('CAIRIS_CFG environment variable has not been set.  Please set this to the correct location of your CAIRIS configuration file, e.g. export CAIRIS_CFG=/home/cairisuser/cairis.cnf') 

  if not os.path.exists(cfgFileName):
    raise ARMException('Unable to locate configuration file at the following location:' + cfgFileName)
  cfgDict = {}
  cfgFile = open(cfgFileName)
  for cfgLine in cfgFile.readlines():
    cfgTuple = cfgLine.split('=')
    if len(cfgTuple) != 2:
      pass
    else:
      cfgDict[strip(cfgTuple[0])] = strip(cfgTuple[1])
  cfgFile.close()
  return cfgDict

def initialiseCairisDbSettings(cfgDict):
  b = Borg()
  b.dbHost = cfgDict['dbhost']
  b.dbPort = int(cfgDict['dbport'])
  b.dbUser = cfgDict['dbuser']
  b.dbPasswd = cfgDict['dbpasswd']
  b.dbName = cfgDict['dbname']
  b.tmpDir = cfgDict['tmp_dir']
  b.cairisRoot = cfgDict['root']
  b.imageDir = os.path.abspath(cfgDict['default_image_dir'])


def setupDocBookConfig():
  b = Borg()
  b.docBookDir = 'http://www.docbook.org/sgml/4.5'
  if os.path.exists('/usr/share/sgml/docbook/dtd/4.5'):
    b.docBookDir = '/usr/share/sgml/docbook/dtd/4.5'
  else:
    b.logger.warning('Unable to find DocBook schemes. Check if DocBook is correctly installed.')

def initialiseDesktopSettings():
  b = Borg()
  pSettings = b.dbProxy.getProjectSettings()
  b.fontSize = pSettings['Font Size']
  b.apFontSize = pSettings['AP Font Size']
  b.fontName = pSettings['Font Name']
  b.mainFrame = None

def initialise():
  cfgDict = parseConfigFile()
  initialiseCairisDbSettings(cfgDict)

  b = Borg()
  b.runmode = 'desktop'
  b.logger = logging.getLogger('cairis_gui')
  b.imageDir = b.cairisRoot + '/images' 
  b.configDir = b.cairisRoot + '/config'
  setupDocBookConfig()

  b.dbProxy = DatabaseProxyFactory.build()
  initialiseDesktopSettings()

def dInitialise():
  cfgDict = parseConfigFile()
  initialiseCairisDbSettings(cfgDict)

  b = Borg()
  b.runmode = 'web'
  b.logger = logging.getLogger('cairisd')
  b.imageDir = os.path.join(b.cairisRoot,'images')
  b.configDir = os.path.join(b.cairisRoot,'config')

  b.uploadDir = cfgDict['upload_dir']
  try:
    b.webPort = int(cfgDict['web_port'])
  except TypeError, ex:
    b.logger.error(str(ex.message))

  if cfgDict['log_level'].lower() == 'debug':
    b.logLevel = logging.DEBUG
  elif cfgDict['log_level'].lower() == 'none':
    b.logLevel = logging.FATAL
  elif cfgDict['log_level'].lower() == 'info':
    b.logLevel = logging.INFO
  elif cfgDict['log_level'].lower() == 'error':
    b.logLevel = logging.ERROR
  else:
    b.logLevel = logging.WARNING

  b.staticDir = cfgDict['web_static_dir']
  b.templateDir = os.path.join(b.cairisRoot,'templates')
  if not hasattr(b, 'uploadDir'):
    b.uploadDir = os.path.join(b.cairisRoot,'cairis/static')

  paths = {
    'root': b.cairisRoot,
    'image': b.imageDir,
    'configuration files': b.configDir,
    'template files': b.templateDir,
    'upload': b.uploadDir
  }

  for key, path in paths.items():
    if not os.path.exists(path):
      err_msg = 'The {0} directory of CAIRIS is inaccessible or not existing.{1}Path: {2}'.format(key, os.linesep, path)
      b.logger.error(err_msg)
      exit(6)

  image_upload_dir = os.path.join(b.uploadDir, 'images')
  if os.path.exists(image_upload_dir):
    try:
      test_file = os.path.join(image_upload_dir, 'test.txt')
      fs_test = open(test_file, 'wb')
      fs_test.write('test')
      fs_test.close()
      os.remove(test_file)
    except IOError:
      err_msg = 'The upload directory for images is not writeable. Image uploading will propably not work.'
      b.logger.warning(err_msg)
  else:
    try:
      os.mkdir(image_upload_dir, 0775)
    except IOError:
      err_msg = 'Unable to create directory to store images into. Image uploading will probably not work.'
      b.logger.warning(err_msg)

  b.template_generator = TemplateGenerator()
  b.model_generator = GraphicsGenerator('svg')

  b.settings = dict()
  b.settings['test'] = {
    'session_id': 'test',
    'fontSize': '13',
    'fontName': 'Times New Roman',
    'jsonPrettyPrint': True,
    'apFontSize': '7.5',
    'dbHost': b.dbHost,
    'dbPort': b.dbPort,
    'dbUser': b.dbUser,
    'dbPasswd': b.dbPasswd,
    'dbName': b.dbName
  }

  db_proxy = MySQLDatabaseProxy(
    host = b.settings['test']['dbHost'],
    port = b.settings['test']['dbPort'],
    user = b.settings['test']['dbUser'],
    passwd = b.settings['test']['dbPasswd'],
    db = b.settings['test']['dbPasswd'])

  if db_proxy.conn.open:
    db_proxy.close()

  b.settings['test']['dbProxy'] = db_proxy
  b.dbProxy = db_proxy
