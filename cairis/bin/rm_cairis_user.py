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
from cairis.core.dba import dropUser,accounts

__author__ = 'Shamal Faily'


def main():
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Remove CAIRIS user')
  parser.add_argument('user',help='Account (email) name.  "all" removes all accounts')
  args = parser.parse_args()

  cairis.core.BorgFactory.dInitialise()
  b = Borg()
  if (args.user.upper() == 'ALL'):
    for user in accounts(b.rPasswd, b.dbHost, b.dbPort):
      dropUser(b.rPasswd, b.dbHost, b.dbPort, user)

  else:
    dropUser(b.rPasswd, b.dbHost, b.dbPort, args.user)

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print('Fatal rm_cairis_user error: ' + str(e))
    sys.exit(-1)

