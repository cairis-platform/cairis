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

import argparse
import sys
from cairis.core.Borg import Borg
import cairis.core.BorgFactory
from cairis.core.dba import grantDatabaseAccess, revokeDatabaseAccess

__author__ = 'Shamal Faily'

def main(args=None):
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Update database privileges')
  parser.add_argument('--database',dest='db',default='', help='Database name')
  parser.add_argument('--user',dest='userName',default='',help='CAIRIS user id')
  parser.add_argument('--privilege',dest='permission',default='',help='grant or revoke')
  args = parser.parse_args() 

  if (args.db == ''):
    raise Exception('Database name not set')

  if (args.userName == ''):
    raise Exception('User id not set')

  if (args.permission == ''):
    raise Exception('Privilege not set')

  if (args.permission != 'grant' and args.permission != 'revoke'):
    raise Exception('Invalid privilege')

  cairis.core.BorgFactory.dInitialise()
  b = Borg()
  
  if (args.permission == 'grant'):
    grantDatabaseAccess(b.rPasswd, b.dbHost, b.dbPort, args.db, args.userName) 
  else:
    revokeDatabaseAccess(b.rPasswd, b.dbHost, b.dbPort, args.db, args.userName) 

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print('Fatal dbctl error: ' + str(e))
    sys.exit(-1)
