#!/usr/bin/python3
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
import argparse
import sys
from cairis.core.Borg import Borg
import cairis.core.BorgFactory
from cairis.core.dba import resetUser,accounts
from cairis.mio.ModelExport import exportPackage
from cairis.bin.cimport import package_import

__author__ = 'Shamal Faily'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('reset_user')


def resetDatabase(cairisRoot,rPasswd,dbHost,dbPort,user,isReload,ignoreValidityCheck):
  cairis.core.BorgFactory.initialise(user=user,db='default')
  b = Borg()

  packageFile = '/tmp/' + user + '.cairis'
  if (isReload == '1'):
    logger.info('Exporting ' + user + ' default database')
    exportPackage(packageFile,b.dbProxy,ignoreValidityCheck)

  logger.info('Resetting ' + user)
  resetUser(cairisRoot,rPasswd, dbHost, dbPort, user)

  cairis.core.BorgFactory.initialise(user=user,db='default')
  if (isReload == '1'):
    logger.info('Re-importing ' + user + ' default database')
    pkgStr = open(packageFile,'rb').read()
    package_import(pkgStr)

def main():
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Reset CAIRIS user')
  parser.add_argument('user',help='Email address or all for all users')
  parser.add_argument('--reload',dest='isReload',help='If 1 is set, reload the contents of the default database', default='0')
  parser.add_argument('--ignore_validity',dest='ignoreValidityCheck',help='If 1 is set, databases will not be validity checked before export', default=0)

  args = parser.parse_args()

  cairis.core.BorgFactory.dInitialise()
  b = Borg()
  
  if (args.user != 'all'):
    resetDatabase(b.cairisRoot,b.rPasswd,b.dbHost,b.dbPort,args.user,args.isReload,args.ignoreValidityCheck)
  else:
    for email in accounts(b.cairisRoot,b.dbHost,b.dbPort):
      resetDatabase(b.cairisRoot,b.rPasswd,b.dbHost,b.dbPort,email,args.isReload,args.ignoreValidityCheck)

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print('Fatal reset_cairis_user error: ' + str(e))
    sys.exit(-1)

