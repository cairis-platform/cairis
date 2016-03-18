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

if __name__ == '__main__':

  rootDir = ''
  try:
    rootDir = os.environ['CAIRIS_DIR']
  except KeyError:
    rootDir = os.environ['PWD']
  sys.path.append(rootDir + '/core')
  sys.path.append(rootDir + '/gui')
  sys.path.append(rootDir + '/mio')

  import BorgFactory
  from ModelExport import *
  from ARM import *

  try:
    parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Model Export to Redmine')
    parser.add_argument('outputFile',help='output file name')
    parser.add_argument('--type',dest='modelFormat',help='model type to export.  One of all, requirements, scenarios, usecases, architecture, attackpatterns or GRL')
#    parser.add_argument('--persona',dest='personaName',help='Persona name (relevant for GRL export only)')
    parser.add_argument('--persona',nargs='+',help='Persona name (relevant for GRL export only)')
#    parser.add_argument('--task',dest='taskName',help='Task name (relevant for GRL export only)')
    parser.add_argument('--task',nargs='+',help='Task name (relevant for GRL export only)')
    parser.add_argument('--environment',dest='envName',help='Environment name (relevant for GRL export only)')
    args = parser.parse_args() 
    BorgFactory.initialise()
   
    msgStr = ''
    if (args.modelFormat == 'all'):
      msgStr += exportModel(args.outputFile)
    elif (args.modelFormat == 'scenarios'):
      msgStr += exportRedmineScenarios(args.outputFile)
    elif (args.modelFormat == 'requirements'):
      msgStr += exportRedmineRequirements(args.outputFile)
    elif (args.modelFormat == 'usecases'):
      msgStr += exportRedmineUseCases(args.outputFile)
    elif (args.modelFormat == 'architecture'):
      msgStr += exportArchitecture(args.outputFile)
    elif (args.modelFormat == 'attackpatterns'):
      msgStr += exportAttackPatterns(args.outputFile)
    elif (args.modelFormat == 'GRL'):
      personaNames = []
      personaNames.extend(args.persona)
      taskNames = []
      taskNames.extend(args.task)

      if len(personaNames) == 0:
        raise ARMException('Persona name not specified for GRL export')
      elif len(taskNames) == 0:
        raise ARMException('Task name not specified for GRL export')
      elif args.envName == None:
        raise ARMException('Environment name not specified for GRL export')
      else:
        msgStr += exportGRL(args.outputFile,personaNames,taskNames,args.envName)
    else:
      raise ARMException('Export model type ' + args.modelFormat + ' not recognised')
    print msgStr
  except ARMException, e:
    print 'cexport error: ',e
    exit(-1) 
