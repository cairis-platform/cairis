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
from cairis.core.ARM import ARMException

__author__ = 'Shamal Faily'

def main(args=None):
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Model Import')
  parser.add_argument('modelFile',help='model file to import')
  parser.add_argument('--user',dest='userName',help='user name', default='cairis_test')
  parser.add_argument('--database',dest='dbName',help='database name',default='cairis_test')
  parser.add_argument('--type',dest='modelFormat',help='model type to import.  One of securitypattern, attackpattern, tvtypes, directory, requirements, riskanalysis, usability, misusability, project, domainvalues, architecturalpattern, associations, synopses, processes, assets, locations, dataflows or all',default='all')
  parser.add_argument('--overwrite',dest='isOverwrite',help='Where appropriate, overwrite an existing CAIRIS model with this model',default=1)
  parser.add_argument('--image_dir',dest='imageDir',help='Where appropriate, directory for model images (overwrites default_image_dir value in cairis.cnf)')
  args = parser.parse_args() 
  mFormat = args.modelFormat
  importFile = args.modelFile
  overwriteFlag = args.isOverwrite
  import cairis.core.BorgFactory
  from cairis.core.Borg import Borg
  cairis.core.BorgFactory.initialise(user=args.userName,db=args.dbName)
  b = Borg()
  if args.imageDir != None:
    b.imageDir = os.path.abspath(args.imageDir)
  file_import(importFile,mFormat,overwriteFlag)

def file_import(importFile,mFormat,overwriteFlag,session_id = None):
  if overwriteFlag == None:
    overwriteFlag = 1

  if (os.access(importFile, os.R_OK)) == False:
    raise ARMException("Cannot access " + importFile)

  from cairis.mio.ModelImport import importSecurityPatternsFile, importAttackPattern,importTVTypeFile,importDirectoryFile,importRequirementsFile, importRiskAnalysisFile, importUsabilityFile, importAssociationsFile, importProjectFile, importDomainValuesFile, importComponentViewFile, importSynopsesFile,importProcessesFile,importAssetsFile,importLocationsFile,importModelFile,importMisusabilityFile,importDataflowsFile

  msgStr = ''
  if (mFormat == 'securitypattern' or mFormat == 'Security Pattern'):
    msgStr += importSecurityPatternsFile(importFile,session_id)
  elif (mFormat == 'attackpattern' or mFormat == 'Attack Pattern'):
    msgStr += importAttackPattern(importFile,session_id)
  elif (mFormat == 'tvtypes' or mFormat == 'Threat and Vulnerability Types'):
    msgStr += importTVTypeFile(importFile,int(overwriteFlag),session_id)
  elif (mFormat == 'directory' or mFormat == 'Threat and Vulnerability Directory'):
    msgStr += importDirectoryFile(importFile,int(overwriteFlag),session_id)
  elif (mFormat == 'requirements' or mFormat == 'Requirements'):
    msgStr += importRequirementsFile(importFile,session_id)
  elif (mFormat == 'riskanalysis' or mFormat == 'Risk Analysis'):
    msgStr += importRiskAnalysisFile(importFile,session_id)
  elif (mFormat == 'usability' or mFormat == 'Usability'):
    msgStr += importUsabilityFile(importFile,session_id)
  elif (mFormat == 'misusability' or mFormat == 'Misusability'):
    msgStr += importMisusabilityFile(importFile,session_id)
  elif (mFormat == 'associations' or mFormat == 'Associations'):
    msgStr += importAssociationsFile(importFile,session_id)
  elif (mFormat == 'project' or mFormat == 'Project data'):
    msgStr += importProjectFile(importFile,session_id)
  elif (mFormat == 'domainvalues' or mFormat == 'Domain Values'):
    msgStr += importDomainValuesFile(importFile,session_id)
  elif (mFormat == 'architecturalpattern' or mFormat == 'Architectural Pattern'):
    msgStr += importComponentViewFile(importFile,session_id)
  elif (mFormat == 'synopses' or mFormat == 'Synopses'):
    msgStr += importSynopsesFile(importFile,session_id)
  elif (mFormat == 'processes' or mFormat == 'Processes'):
    msgStr += importProcessesFile(importFile,session_id)
  elif (mFormat == 'assets' or mFormat == 'Assets'):
    msgStr += importAssetsFile(importFile,session_id)
  elif (mFormat == 'locations' or mFormat == 'Locations'):
    msgStr += importLocationsFile(importFile,session_id)
  elif (mFormat == 'dataflows' or mFormat == 'Dataflows'):
    msgStr += importDataflowsFile(importFile,session_id)
  elif (mFormat == 'all' or mFormat == 'Model'):
    msgStr += importModelFile(importFile,int(overwriteFlag),session_id)
  else:
    raise ARMException('Input model type ' + mFormat + ' not recognised')
  return 0

if __name__ == '__main__':
  try:
    from cairis.core.ARM import ARMException
    main()
  except ImportError as e:
    print("Fatal CAIRIS error: " + str(e))
    sys.exit(-1)
  except ARMException as e:
    print('Fatal cimport error: ' + str(e))
    sys.exit(-1)

