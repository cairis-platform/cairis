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

__author__ = 'Shamal Faily'

from .AssetParameters import AssetParameters
from .AssetEnvironmentProperties import AssetEnvironmentProperties
from .RoleParameters import RoleParameters
from .UseCaseParameters import UseCaseParameters
from .UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from .Step import Step
from .Steps import Steps
from cairis.core.Borg import Borg

def build(objtName,envName,objtType,session_id = None,objtParameter = None):
  if (objtType == 'asset'):
    return addDefaultAsset(objtName,envName,session_id,objtParameter)
  elif (objtType == 'usecase'):
    return addDefaultUseCase(objtName,envName,session_id)
  else:
    raise ARMException("Cannot build default object " + objtName + ".  " + objtType + " not a supported dimension.")

def addDefaultAsset(objtName,envName,session_id,assetType= 'Information'):
  assetDesc = 'To be defined'
  shortCode = 'TBD'
  significanceText = 'To be defined'
  b = Borg()
  dbProxy = b.get_dbproxy(session_id)
  envProps = [AssetEnvironmentProperties(envName,[0,0,1,0,0,0,0,0],['None','None','To be defined','None','None','None','None','None'])]
  p = AssetParameters(objtName,shortCode,assetDesc,significanceText,assetType,False,'',[],[],envProps)
  return dbProxy.addAsset(p)

def addDefaultUseCase(objtName,envName,session_id):
  b = Borg()
  dbProxy = b.get_dbproxy(session_id)
  roleId = dbProxy.existingObject('Unknown','role')
  if (roleId == -1):
    roleId = dbProxy.addRole(RoleParameters('Unknown','Stakeholder','UNKNOWN','Unknown role',None))
  
  s = Steps()
  s.append(Step('Undefined'))
  envProps = [UseCaseEnvironmentProperties(envName,'To be defined',s,'To be defined')]
  p = UseCaseParameters(objtName,'Unknown','TBC',['Unknown'],'To be defined',[],envProps)
  return dbProxy.addUseCase(p)
