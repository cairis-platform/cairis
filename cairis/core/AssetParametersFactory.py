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
from .Response import Response
from .Borg import Borg

def build(target,dbProxy = None):
  if target.__class__.__name__ == 'Countermeasure':
    return buildCMAsset(target,dbProxy)

def buildCMAsset(target,proxy):
  assetName = target.name() + ' CM'
  assetDesc = target.description()
  assetType = target.type()
  shortCode = 'XX'
  significanceText = 'Mitigates risk '
  risks = proxy.mitigatedRisks(target.id())
  significanceText += risks[0]
  assetEnvironmentProperties = []
  for cProps in target.environmentProperties():
    assetEnvironmentProperties.append(AssetEnvironmentProperties(cProps.name(),cProps.properties(),cProps.rationale()))
  return AssetParameters(assetName,shortCode,assetDesc,significanceText,assetType,False,'',target.tags(),[],assetEnvironmentProperties)

def buildFromTemplate(assetName,assetEnvs,dbProxy = None):
  if (dbProxy == None):
    b = Borg()
    dbProxy = b.dbProxy
  taObjt = dbProxy.dimensionObject(assetName,'template_asset')
  assetDesc = taObjt.description()
  assetType = taObjt.type()
  shortCode = taObjt.shortCode()
  significanceText = taObjt.significance()
  assetEnvironmentProperties = []
  secProperties = taObjt.securityProperties()
  pRationale = taObjt.rationale()
  tags = taObjt.tags()
  ifs = taObjt.interfaces()
  for envName in assetEnvs:
    assetEnvironmentProperties.append(AssetEnvironmentProperties(envName,secProperties,pRationale))
  return AssetParameters(assetName,shortCode,assetDesc,significanceText,assetType,False,'',tags,ifs,assetEnvironmentProperties)  
