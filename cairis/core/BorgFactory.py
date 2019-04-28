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

__author__ = 'Shamal Faily, Robin Quetin'

from .Borg import Borg
import os
import logging
import json
from cairis.tools.GraphicsGenerator import GraphicsGenerator
from .MySQLDatabaseProxy import MySQLDatabaseProxy
from .ARM import ARMException
from .PasswordManager import getDatabasePassword

def testUploadDirectory(uploadDir,logger):
  
  image_upload_dir = os.path.join(uploadDir, 'images')
  if os.path.exists(image_upload_dir):
    try:
      test_file = os.path.join(image_upload_dir, 'test.txt')
      fs_test = open(test_file, 'wb')
      fs_test.write('test'.encode('utf-8'))
      fs_test.close()
      os.remove(test_file)
    except IOError:
      err_msg = 'The upload directory for images is not writeable. Image uploading will propably not work.'
      logger.warning(err_msg)
  else:
    try:
      os.mkdir(image_upload_dir, 0o775)
    except IOError:
      err_msg = 'Unable to create directory to store images into. Image uploading will probably not work.'
      logger.warning(err_msg)


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
      cfgDict[cfgTuple[0].strip()] = cfgTuple[1].strip()
  cfgFile.close()
  return cfgDict

def initialiseCairisDbSettings(cfgDict):
  b = Borg()
  b.dbHost = cfgDict['dbhost']
  b.dbPort = int(cfgDict['dbport'])
  b.dbUser = 'cairis_test'
  b.dbPasswd = 'cairis_test'
  b.dbName = 'cairis_test_default'
  b.tmpDir = cfgDict['tmp_dir']
  b.cairisRoot = cfgDict['root']
  b.imageDir = os.path.abspath(cfgDict['default_image_dir'])
  b.rPasswd = ''
  b.docker = True if 'docker' in cfgDict else False
  
  try:
    b.rPasswd = cfgDict['rpasswd']
  except KeyError:
    pass

def setupDocBookConfig():
  b = Borg()
  b.docBookDir = 'http://www.docbook.org/sgml/4.5'
  if os.path.exists('/usr/share/sgml/docbook/dtd/4.5') or b.docker:
    b.docBookDir = '/usr/share/sgml/docbook/dtd/4.5'
  else:
    b.logger.warning('Unable to find DocBook schemes. Check if DocBook is correctly installed.')
  tf = open(b.configDir + '/sizes.json')
  b.objtSizes = json.load(tf)
  tf.close()

def initialiseDesktopSettings():
  b = Borg()
  pSettings = b.dbProxy.getProjectSettings()
  b.fontSize = pSettings['Font Size']
  b.apFontSize = pSettings['AP Font Size']
  b.fontName = pSettings['Font Name']
  b.mainFrame = None

def initialise(user='cairis_test',db='cairis_test_default'):
  cfgDict = parseConfigFile()
  initialiseCairisDbSettings(cfgDict)

  b = Borg()
  b.runmode = 'desktop'
  logging.basicConfig()
  b.logger = logging.getLogger('cairis_gui')
  b.iconDir = b.cairisRoot + '/images' 
  b.configDir = b.cairisRoot + '/config'
  setupDocBookConfig()

  from cairis.gui.GUIDatabaseProxy import GUIDatabaseProxy
  dbPasswd = ''
  if (user == 'cairis_test'):
    dbPasswd = 'cairis_test'
    db='cairis_test_default'
  else:
    b.dbUser = user
    dbPasswd = getDatabasePassword(user)
    b.dbPasswd = dbPasswd
    b.dbName = db
  b.dbProxy = GUIDatabaseProxy(user=user,passwd=b.dbPasswd,db=db)
  initialiseDesktopSettings()

def dInitialise(withTest = True):
  cfgDict = parseConfigFile()
  initialiseCairisDbSettings(cfgDict)

  b = Borg()
  b.runmode = 'web'
  logging.basicConfig()
  b.logger = logging.getLogger('cairisd')
  b.configDir = os.path.join(b.cairisRoot,'config')
  b.uploadDir = cfgDict['upload_dir']
  b.secretKey = cfgDict['secret_key']

  try:
    b.webPort = int(cfgDict['web_port'])
  except TypeError as ex:
    b.logger.error(str(ex.message))

  if cfgDict['log_level'].lower() == 'debug': b.logLevel = logging.DEBUG
  elif cfgDict['log_level'].lower() == 'none': b.logLevel = logging.FATAL
  elif cfgDict['log_level'].lower() == 'info': b.logLevel = logging.INFO
  elif cfgDict['log_level'].lower() == 'error': b.logLevel = logging.ERROR
  else:
    b.logLevel = logging.WARNING

  b.staticDir = cfgDict['web_static_dir']

  if ('web_asset_dir' not in cfgDict):
    b.assetDir = b.staticDir
  else: 
    b.assetDir = cfgDict['web_asset_dir']
  b.templateDir = os.path.join(b.cairisRoot,'templates')
  if not hasattr(b, 'uploadDir'): b.uploadDir = os.path.join(b.cairisRoot,'cairis/static')

  paths = {
    'root': b.cairisRoot,
    'image': b.imageDir,
    'configuration files': b.configDir,
    'template files': b.templateDir,
    'upload': b.uploadDir
  }

  for key, path in list(paths.items()):
    if not os.path.exists(path):
      err_msg = 'The {0} directory of CAIRIS is inaccessible or not existing.{1}Path: {2}'.format(key, os.linesep, path)
      b.logger.error(err_msg)
      exit(6)

  testUploadDirectory(b.uploadDir,b.logger)

  b.model_generator = GraphicsGenerator('svg')

  b.settings = dict()


  b.settings['test'] = {
    'session_id': 'test',
    'fontSize': '13',
    'fontName': 'Times New Roman',
    'jsonPrettyPrint': True,
    'apFontSize': '7.5',
    'dbUser': 'cairis_test',
    'userName' : 'CAIRIS test user account',
    'dbPasswd' : 'cairis_test',
    'dbName' : 'cairis_test_default',
    'dbHost': b.dbHost,
    'dbPort': b.dbPort,
    'rPasswd': b.rPasswd
  }
  db_proxy = MySQLDatabaseProxy(
    host = b.settings['test']['dbHost'],
    port = b.settings['test']['dbPort'],
    user = b.settings['test']['dbUser'],
    passwd = b.settings['test']['dbPasswd'],
    db = b.settings['test']['dbName'])
  if db_proxy.conn is not None:
    db_proxy.close()

  b.settings['test']['dbProxy'] = db_proxy
  b.dbProxy = db_proxy
  b.fontSize = '13'
  b.apFontSize = '7.5'
  b.fontName = 'Times New Roman'

  setupDocBookConfig()
