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

import pydot
from cairis.core.ARM import *
from cairis.daemon.CairisHTTPError import CairisHTTPError, ARMHTTPError
from cairis.data.CairisDAO import CairisDAO
from cairis.bin.cimport import file_import, package_import
from cairis.bin.at2om import dotToObstacleModel
from cairis.mio.ModelImport import importAttackTreeString
from cairis.mio.ModelImport import importDiagramsNetDFD, importDiagramsNetAssetModel, importUserGoalWorkbook, importPersonaCharacteristicsWorkbook
from cairis.core.Borg import Borg
from zipfile import ZipFile
import magic
import io
import os

__author__ = 'Shamal Faily'


class ImportDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def package_import(self,pkgStr):
    return package_import(pkgStr,self.session_id)

  def file_import(self,importFile,mFormat,overwriteFlag):
    return file_import(importFile,mFormat,overwriteFlag,self.session_id)

  def diagramsnet_import(self,importFile,modelType,environment_name):
    try:
      if (modelType == 'diagrams.net (Data Flow Diagram)'):
        return importDiagramsNetDFD(importFile,environment_name,self.session_id)
      elif (modelType == 'diagrams.net (Asset Model)'):
        return importDiagramsNetAssetModel(importFile,environment_name,self.session_id)
      else:
        raise ARMException(modelType + " is an invalid model type.")
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
  
  def import_attack_tree(self,dotBuf,environment_name,contributor_name):
    try:
      dotInstance = pydot.graph_from_dot_data(dotBuf)
      xmlBuf = dotToObstacleModel(dotInstance[0],environment_name,contributor_name)
      return importAttackTreeString(xmlBuf,self.session_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def import_user_goals(self,wbStr):
    return importUserGoalWorkbook(wbStr,self.session_id)

  def import_persona_characteristics(self,wbStr):
    return importPersonaCharacteristicsWorkbook(wbStr,self.session_id)
