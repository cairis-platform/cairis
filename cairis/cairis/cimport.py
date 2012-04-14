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
from ModelImport import *
from ARM import *


if __name__ == '__main__':
  try:
    parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Model Import')
    parser.add_argument('modelFile',help='model file to import')
    parser.add_argument('--import',dest='modelFormat',help='model type to import.  One of securitypattern, tvtypes, directory, requirements, riskanalysis, usability, project, domainvalues, component or all')
    args = parser.parse_args() 
    mFormat = args.modelFormat
    importFile = args.modelFile

    BorgFactory.initialise()
   
    msgStr = ''
    if (mFormat == 'securitypattern'):
      msgStr += importSecurityPatterns(importFile)
    elif (mFormat == 'tvtypes'):
      msgStr += importTVTypeFile(importFile)
    elif (mFormat == 'directory'):
      msgStr += importDirectoryFile(importFile)
    elif (mFormat == 'requirements'):
      msgStr += importRequirementsFile(importFile)
    elif (mFormat == 'riskanalysis'):
      msgStr += importRiskAnalysisFile(importFile)
    elif (mFormat == 'usability'):
      msgStr += importUsabilityFile(importFile)
    elif (mFormat == 'associations'):
      msgStr += importAssociationsFile(importFile)
    elif (mFormat == 'project'):
      msgStr += importProjectFile(importFile)
    elif (mFormat == 'domainvalues'):
      msgStr += importDomainValuesFile(importFile)
    elif (mFormat == 'component'):
      msgStr += importComponentViewFile(importFile)
    elif (mFormat == 'all'):
      msgStr += importModelFile(importFile)
    else:
      raise ARMException('Input model type ' + mFormat + ' not recognised')
    print msgStr
  except ARMException, e:
    print 'cimport error: ',e
    exit(-1) 
