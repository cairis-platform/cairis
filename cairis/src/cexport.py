#!/usr/bin/python
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
