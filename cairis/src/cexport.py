#!/usr/bin/python
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


#$URL$

import argparse
import BorgFactory
from ModelExport import *
from ARM import *


if __name__ == '__main__':
  try:
    parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Model Export to Redmine')
    parser.add_argument('outputFile',help='output file name')
    parser.add_argument('--export',dest='modelFormat',help='model type to export.  One of requirements, scenarios, or usecases')
    args = parser.parse_args() 

    BorgFactory.initialise()
   
    msgStr = ''
    if (args.modelFormat == 'scenarios'):
      msgStr += exportRedmineScenarios(args.outputFile)
    elif (args.modelFormat == 'requirements'):
      msgStr += exportRedmineRequirements(args.outputFile)
    elif (args.modelFormat == 'usecases'):
      msgStr += exportRedmineUseCases(args.outputFile)
    else:
      raise ARMException('Export model type ' + args.modelFormat + ' not recognised')
    print msgStr
  except ARMException, e:
    print 'cexport error: ',e
    exit(-1) 
