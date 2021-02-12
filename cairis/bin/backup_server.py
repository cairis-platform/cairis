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
import tarfile
import os
from cairis.core.ARM import ARMException
from cairis.core.Borg import Borg
import cairis.core.BorgFactory
from cairis.core.dba import accounts,canonicalDbUser,dbtoken,emailHashes
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy
from cairis.mio.ModelExport import exportPackage

__author__ = 'Shamal Faily'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('backup_server')


def main():
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Backup server')
  parser.add_argument('tarArchive',help='Model archive tarball to be created ')
  args = parser.parse_args()

  cairis.core.BorgFactory.initialise()
  b = Borg()
  
  aNames = accounts(b.rPasswd,b.dbHost,b.dbPort)
  for email in aNames:
    userPasswd = dbtoken(b.rPasswd,b.dbHost,b.dbPort,email)
    dbUser = canonicalDbUser(email)
    dbName = dbUser + '_default'
    dbProxy = MySQLDatabaseProxy(b.dbHost,b.dbPort,dbUser,userPasswd,dbName)
    packageFile = b.tmpDir + '/' + email + '.cairis'
    try:
      exportPackage(packageFile,None,0,dbProxy)
      logger.info('Exported ' + email + ' default database')
    except ARMException as ex:
      logger.info('Error exporting ' + email + ' default database : ' + str(ex))
      exportPackage(packageFile,None,1,dbProxy)
      logger.info('Exported ' + email + ' default database by ignoring validity checks')
    dbProxy.close()

  with tarfile.open(args.tarArchive,'w') as archive:
    for p in os.listdir(b.tmpDir):
      modelName = b.tmpDir + '/' + p
      archive.add(modelName, arcname=p, filter=lambda x: x if x.name.endswith('.cairis') else None)
    hashFile = b.tmpDir + '/hashes.txt'
    with open(hashFile,'w') as f:
      f.write('\n'.join(list(map(lambda x : ','.join(x),emailHashes(b.rPasswd,b.dbHost,b.dbPort)))))
    archive.add(hashFile, arcname='hashes.txt')
if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print('Fatal backup_server error: ' + str(e))
    sys.exit(-1)

