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
from cairis.bin.cimport import file_import
from cairis.bin.at2om import dotToObstacleModel
from cairis.mio.ModelImport import importAttackTreeString
from cairis.core.Borg import Borg
from zipfile import ZipFile
import magic
import io
import os
import xml.etree.ElementTree as ET

__author__ = 'Shamal Faily'


class ImportDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def package_import(self,pkgStr):
    try:
      b = Borg()
      buf = io.BytesIO(pkgStr)
      zf = ZipFile(buf)
      fileList = zf.namelist()
      
      modelImages = []
      models = {'cairis_model' : '', 'locations' : [], 'architectural_pattern' : [], 'security_patterns' : []}

      for fileName in fileList:
        fName,fType = fileName.split('.')
        if (fType == 'xml'):
          zf.extract(fileName,b.tmpDir)
          modelType = ET.fromstring(open(b.tmpDir + '/' + fileName).read()).tag
          os.remove(b.tmpDir + '/' + fileName)
          if (modelType == 'cairis_model'):
            if (models[modelType] != ''):
              raise ARMHTTPError('Cannot have more than one CAIRIS model file in the package file')
            models[modelType] = fileName
          else:
            models[modelType].append(fileName)
        else:
          modelImages.append(fileName)

      cairisModel = models['cairis_model']
      if (cairisModel == ''):
        raise ARMHTTPError('No CAIRIS model file in the package file')
      else:
        zf.extract(cairisModel,b.tmpDir)
        self.file_import(b.tmpDir + '/' + cairisModel,'all',1) 
        os.remove(b.tmpDir + '/' + cairisModel)

      for typeKey in ['locations','architectural_pattern','security_patterns']:
        for modelFile in models[typeKey]:
          zf.extract(modelFile,b.tmpDir)
          if (typeKey == 'architectural_pattern'):
            typeKey = 'architecturalpattern'
          elif (typeKey == 'security_patterns'):
            typeKey = 'securitypattern'
          self.file_import(b.tmpDir + '/' + modelFile,typeKey,0) 
          os.remove(b.tmpDir + '/' + modelFile)
      for imageFile in modelImages:
        buf = zf.read(imageFile)
        mimeType = magic.from_buffer(buf,mime=True)
        self.db_proxy.setImage(imageFile,buf,mimeType)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def file_import(self,importFile,mFormat,overwriteFlag):
    try:
      return file_import(importFile,mFormat,overwriteFlag,self.session_id)
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
