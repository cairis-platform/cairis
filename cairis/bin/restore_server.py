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
from cairis.core.dba import accounts,canonicalDbUser,dbtoken,updateEmailHashes
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy
from cairis.mio.ModelExport import exportPackage
from cairis.bin.add_cairis_user import addCairisUser
from cairis.bin.cimport import package_import

__author__ = 'Shamal Faily'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('restore_server')


def main():
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Restore server')
  parser.add_argument('archiveFile',help='Model archive tarball to be restored')
  args = parser.parse_args()

  cairis.core.BorgFactory.initialise()
  b = Borg()

  modelFiles = []
  models = []
  hashes = []
  with tarfile.open(args.archiveFile,'r') as archive:
    modelFiles = archive.getmembers()
    for modelFile in modelFiles:
      if (modelFile.name != 'hashes.txt'):
        accountName = modelFile.name.split('.cairis')[0]
        try:
          addCairisUser(accountName,accountName,accountName)
          models.append((accountName,archive.extractfile(modelFile).read()))
          logger.info('Re-created account ' + accountName)
        except ARMException as ex:
          logger.info('Error re-creating account ' + accountName + ' : ' + str(ex))
      else:
        hashes = list(map(lambda x: x.decode().rstrip().split(','),archive.extractfile(modelFile).readlines()))
    for accountName,model in models:
      try:
        cairis.core.BorgFactory.initialise(user=accountName,db='default')
        package_import(model)
        logger.info('Re-imported default model for account ' + accountName)
      except ARMException as ex:
        logger.info('Error re-importing default model for account ' + accountName + ' : ' + str(ex))
    updateEmailHashes(b.rPasswd,b.dbHost,b.dbPort,hashes)
if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print('Fatal restore_server error: ' + str(e))
    sys.exit(-1)
