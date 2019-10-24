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
import os
import sys
from cairis.tools.quickSetup import quick_setup

__author__ = 'Shamal Faily'

def main(args=None):
  parser = argparse.ArgumentParser(description='CAIRIS server setup script - headless')
  parser.add_argument('--dbHost',dest='dbHost',help='Database host name', default='localhost')
  parser.add_argument('--dbPort',dest='dbPort',help='Database port number',default='3306')
  parser.add_argument('--dbRootPassword',dest='dbRootPassword',help='Database root password',default='')
  parser.add_argument('--tmpDir',dest='tmpDir',help='Temp directory',default='/tmp')
  defaultRootDir = os.path.split(os.path.split(os.path.realpath(os.path.dirname(__file__)))[0])[0]
  parser.add_argument('--rootDir',dest='rootDir',help='Root directory',default=defaultRootDir + '/cairis')
  homeDir = os.environ['HOME']
  parser.add_argument('--configFile',dest='configFile',help='CAIRIS configuration file name (fully qualified path)',default=homeDir + '/cairis.cnf')
  parser.add_argument('--webPort',dest='webPort',help='Web port',default='7071')
  parser.add_argument('--logLevel',dest='logLevel',help='Log level',default='warning')
  parser.add_argument('--staticDir',dest='staticDir',help='Static directory',default=defaultRootDir + '/cairis/dist')
  parser.add_argument('--assetDir',dest='assetDir',help='Asset directory',default=defaultRootDir + '/cairis/dist')
  parser.add_argument('--mailServer',dest='mailServer',help='Mail server',default='')
  parser.add_argument('--mailPort',dest='mailPort',help='Mail port',default='')
  parser.add_argument('--mailUser',dest='mailUser',help='Mail user',default='')
  parser.add_argument('--mailPasswd',dest='mailPasswd',help='Mail password',default='')
  args = parser.parse_args() 
  quick_setup(args.dbHost,int(args.dbPort),args.dbRootPassword,args.tmpDir,args.rootDir,args.configFile,int(args.webPort),args.logLevel,args.staticDir,args.assetDir,'','',args.mailServer,args.mailPort,args.mailUser,args.mailPasswd)

if __name__ == '__main__':
  try:
    from cairis.core.ARM import ARMException
    main()
  except ARMException as e:
    print('Fatal setup error: ' + str(e))
    sys.exit(-1)

