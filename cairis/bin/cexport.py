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
__author__ = 'Shamal Faily'

def main(args=None):
  import cairis.core.BorgFactory
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Model Export')
  parser.add_argument('outputFile',help='output file name')
  parser.add_argument('--user',dest='userName',help='user name', default='cairis_test')
  parser.add_argument('--database',dest='dbName',help='database name',default='cairis_test')
  parser.add_argument('--type',dest='modelFormat',help='model type to export.  One of all, package, requirements, scenarios, usecases, architecture, attackpatterns, securitypatterns or GRL')
  parser.add_argument('--persona',nargs='+',help='Persona name or ALL (relevant for GRL export only)')
  parser.add_argument('--task',nargs='+',help='Task name or ALL (relevant for GRL export only)')
  parser.add_argument('--environment',dest='envName',help='Environment name (relevant for GRL export only)')
  args = parser.parse_args() 
  cairis.core.BorgFactory.initialise(user=args.userName,db=args.dbName)
  file_export(args.modelFormat,args.outputFile,args.persona,args.task,args.envName)

def file_export(modelFormat = 'all', outputFile = None, persona = None, task = None, envName = None, session_id = None):
  from cairis.mio.ModelExport import exportModel,exportRedmineScenarios,exportRedmineRequirements,exportRedmineUseCases,exportArchitecture,exportAttackPatterns,exportGRL,exportSecurityPatterns,exportPackage
  msgStr = ''
  if (modelFormat == 'all'):
    msgStr += exportModel(outputFile,session_id)
  elif (modelFormat == 'package'):
    msgStr += exportPackage(outputFile,session_id)
  elif (modelFormat == 'scenarios'):
    msgStr += exportRedmineScenarios(outputFile,session_id)
  elif (modelFormat == 'requirements'):
    msgStr += exportRedmineRequirements(outputFile,session_id)
  elif (modelFormat == 'usecases'):
    msgStr += exportRedmineUseCases(outputFile,session_id)
  elif (modelFormat == 'architecture'):
    msgStr += exportArchitecture(outputFile,session_id)
  elif (modelFormat == 'attackpatterns'):
    msgStr += exportAttackPatterns(outputFile,session_id)
  elif (modelFormat == 'securitypatterns'):
    msgStr += exportSecurityPatterns(outputFile,session_id)
  elif (modelFormat == 'GRL'):
    personaNames = []
    personaNames.extend(persona)
    taskNames = []
    taskNames.extend(task)

    if len(personaNames) == 0:
      raise ARMException('Persona name not specified for GRL export')
    elif len(taskNames) == 0:
      raise ARMException('Task name not specified for GRL export')
    elif envName == None:
      raise ARMException('Environment name not specified for GRL export')
    else:
      msgStr += exportGRL(outputFile,personaNames,taskNames,envName,session_id)
  else:
    raise ARMException('Export model type ' + modelFormat + ' not recognised')
  return msgStr

if __name__ == '__main__':
  from cairis.core.ARM import ARMException
  try:
    main()
  except ImportError as e:
    print("Fatal cexport error importing modules: " + str(e))
    sys.exit(-1)
  except ARMException as e:
    print('Fatal cexport error: ' + str(e))
    sys.exit(-1)
