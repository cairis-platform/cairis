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

import argparse
import os
import sys
import cairis.core.ARM

def main(args=None):
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Model Import')
  parser.add_argument('modelFile',help='model file to import')
  parser.add_argument('--type',dest='modelFormat',help='model type to import.  One of securitypattern, attackpattern, tvtypes, directory, requirements, riskanalysis, usability, project, domainvalues, architecturalpattern, associations, synopses, processes, assets, locations or all')
  parser.add_argument('--overwrite',dest='isOverwrite',help='Where appropriate, overwrite an existing CAIRIS model with this model')
  parser.add_argument('--image_dir',dest='imageDir',help='Where appropriate, directory for model images (overwrites default_image_dir value in cairis.cnf)')
  args = parser.parse_args() 
  mFormat = args.modelFormat
  importFile = args.modelFile
  overwriteFlag = args.isOverwrite
  import cairis.core.BorgFactory
  from cairis.core.Borg import Borg
  cairis.core.BorgFactory.initialise()
  b = Borg()
  if args.imageDir != None:
    b.imageDir = os.path.abspath(args.imageDir)
  file_import(importFile,mFormat,overwriteFlag)

def file_import(importFile,mFormat,overwriteFlag,session_id = None):
  if overwriteFlag == None:
    overwriteFlag = 1
  from cairis.core.ARM import *

  if (os.access(importFile, os.R_OK)) == False:
    raise ARMException("Cannot access " + importFile)

  from cairis.mio.ModelImport import *
   
  msgStr = ''
  if (mFormat == 'securitypattern' or mFormat == 'Security Pattern'):
    msgStr += importSecurityPatterns(importFile)
  if (mFormat == 'attackpattern' or mFormat == 'Attack Pattern'):
    msgStr += importAttackPattern(importFile)
  elif (mFormat == 'tvtypes' or mFormat == 'Threat and Vulnerability Types'):
    msgStr += importTVTypeFile(importFile,int(overwriteFlag))
  elif (mFormat == 'directory' or mFormat == 'Threat and Vulnerability Directory'):
    msgStr += importDirectoryFile(importFile,int(overwriteFlag))
  elif (mFormat == 'requirements' or mFormat == 'Requirements'):
    msgStr += importRequirementsFile(importFile)
  elif (mFormat == 'riskanalysis' or mFormat == 'Risk Analysis'):
    msgStr += importRiskAnalysisFile(importFile)
  elif (mFormat == 'usability' or mFormat == 'Usability'):
    msgStr += importUsabilityFile(importFile)
  elif (mFormat == 'associations' or mFormat == 'Associations'):
    msgStr += importAssociationsFile(importFile)
  elif (mFormat == 'project' or mFormat == 'Project data'):
    msgStr += importProjectFile(importFile)
  elif (mFormat == 'domainvalues' or mFormat == 'Domain Values'):
    msgStr += importDomainValuesFile(importFile)
  elif (mFormat == 'architecturalpattern' or mFormat == 'Architectural Pattern'):
    msgStr += importComponentViewFile(importFile)
  elif (mFormat == 'synopses' or mFormat == 'Synopses'):
    msgStr += importSynopsesFile(importFile)
  elif (mFormat == 'processes' or mFormat == 'Processes'):
    msgStr += importProcessesFile(importFile)
  elif (mFormat == 'assets' or mFormat == 'Assets'):
    msgStr += importAssetsFile(importFile)
  elif (mFormat == 'locations' or mFormat == 'Locations'):
    msgStr += importLocationsFile(importFile)
  elif (mFormat == 'all' or mFormat == 'Model'):
    msgStr += importModelFile(importFile,int(overwriteFlag))
  else:
    raise ARMException('Input model type ' + mFormat + ' not recognised')

if __name__ == '__main__':
  try:
    main()
  except ImportError:
    print "Fatal CAIRIS error: Could not import the Python dependencies needed by CAIRIS.  Either your Python installation is incomplete, or - if you have downloaded CAIRIS directly from github - PYTHONPATH needs to be set to the root directly of your source installation; this is the same directory that setup.py can be found in."
    sys.exit(-1)
  except ARMException, e:
    print 'Fatal cimport error: ' + str(e)
    sys.exit(-1)

