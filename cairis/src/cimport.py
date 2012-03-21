#!/usr/bin/python
#$URL$

import argparse
import BorgFactory
from ModelImport import *
from ARM import *


if __name__ == '__main__':
  try:
    parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Model Import')
    parser.add_argument('modelFile',help='model file to import')
    parser.add_argument('--import',dest='modelFormat',help='model type to import.  One of securitypattern, tvtypes, directory, requirements, riskanalysis, usability, project, domainvalues, or all')
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
    elif (mFormat == 'all'):
      msgStr += importModelFile(importFile)
    else:
      raise ARMException('Input model type ' + mFormat + ' not recognised')
    print msgStr
  except ARMException, e:
    print 'cimport error: ',e
    exit(-1) 
