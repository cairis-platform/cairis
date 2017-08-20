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

import logging
import os
from cairis.core.Borg import Borg
import cairis.core.BorgFactory

__author__ = 'Robin Quetin'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('cairisd')

def config(settings):
  logger.info('Starting CAIRIS as web daemon')

  if 'configFile' in settings:
    loadSettingsFromFile(settings['configFile'])
  else:
    loadSettingsFromFile()
  if 'staticDir' in settings:
    setStaticDir(settings['staticDir'])
  if 'port' in settings:
    setPort(int(settings['port']))
  if 'loggingLevel' in settings:
    setLoglevel(settings['loggingLevel'])
  if 'unitTesting' in settings:
    setUnitTesting(settings['unitTesting'])

  logParams()

def loadSettingsFromFile():
  logger.info('Loading settings from $CAIRIS_CFG')
  cairis.core.BorgFactory.dInitialise()

def setLoglevel(log_level):
  b = Borg()
  logger.info('Applying log level...')

  log_level = log_level.lower()
  if log_level == 'verbose':
    realLevel = logging.INFO
  elif log_level == 'debug':
    realLevel = logging.DEBUG
  else:
    realLevel = logging.WARNING

  b.logLevel = realLevel

def setPort(port):
  logger.info('Applying web port...')
  b = Borg()
  if port == 0:
    if not hasattr(b, 'webPort'):
      b.webPort = 7071
  else:
    b.webPort = port

def logParams():
  b = Borg()
  logger.info('Config: %s', os.environ['CAIRIS_CFG'])
  if b.logLevel == logging.INFO:
    logger.info('Log level: INFO')
  elif b.logLevel == logging.DEBUG:
    logger.info('Log level: DEBUG')
  elif b.logLevel == logging.WARNING:
    logger.info('Log level: WARNING')

  logger.info('Port: %d', b.webPort)
  logger.info('Static content directory: %s', b.staticDir)
  logger.info('Unit testing: %s', str(b.unit_testing).lower())

def setStaticDir(static_dir):
  logger.info('Setting static web content directory...')
  b = Borg()
  try:
    os.listdir(static_dir)
  except EnvironmentError as ex:
    logger.warning('The directory for static web content is not readable: %s' % ex.strerror)
    logger.warning('Static content may not be available')

  b.staticDir = os.path.abspath(static_dir)

def setUnitTesting(setting=False):
  logger.info('Setting unit testing property...')
  b = Borg()
  b.unit_testing = setting
