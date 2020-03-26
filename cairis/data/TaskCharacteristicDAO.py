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

from cairis.core.ARM import *
from cairis.core.TaskCharacteristic import TaskCharacteristic
from cairis.core.TaskCharacteristicParameters import TaskCharacteristicParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import TaskCharacteristicModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.PseudoClasses import CharacteristicReference

__author__ = 'Shamal Faily'


class TaskCharacteristicDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'task_characteristic')

  def get_objects(self,constraint_id = -1):
    try:
      tcs = self.db_proxy.getTaskCharacteristics(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    tcsKeys = sorted(tcs.keys())
    tcsList = []
    for key in tcsKeys:
      value = tcs[key]
      del value.theId
      tcsList.append(self.convert_tcrs(real_tc=value))
    return tcsList

  def get_object_by_name(self, task_characteristic_name):
    tcs = self.get_objects()
    if tcs is None or len(tcs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Task characteristic')
    for tc in tcs:
      if (tc.characteristic() == task_characteristic_name):
        return tc
    self.close()
    raise ObjectNotFoundHTTPError('Task characteristic:\"' + task_characteristic_name + '\"')

  def add_object(self, tc):
    tcParams = TaskCharacteristicParameters(
      pName=tc.theTaskName,
      modQual=tc.theModQual,
      cDesc=tc.theName,
      pcGrounds=tc.theGrounds,
      pcWarrant=tc.theWarrant,
      pcBacking=[],
      pcRebuttal=tc.theRebuttal)
    try:
      self.db_proxy.addTaskCharacteristic(tcParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object(self,tc,name):
    tcParams = TaskCharacteristicParameters(
      pName=tc.theTaskName,
      modQual=tc.theModQual,
      cDesc=tc.theName,
      pcGrounds=tc.theGrounds,
      pcWarrant=tc.theWarrant,
      pcBacking=[],
      pcRebuttal=tc.theRebuttal)

    try:
      tcId = self.db_proxy.getDimensionId(name,'task_characteristic')
      tcParams.setId(tcId)
      self.db_proxy.updateTaskCharacteristic(tcParams)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided task characteristic')
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      tcId = self.db_proxy.getDimensionId(name,'task_characteristic')
      self.db_proxy.deleteTaskCharacteristic(tcId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, TaskCharacteristicModel.required)
    json_dict['__python_obj__'] = TaskCharacteristic.__module__+'.'+ TaskCharacteristic.__name__
    tc = json_serialize(json_dict)
    tc = json_deserialize(tc)
    tc = self.convert_tcrs(fake_tc=tc)

    if isinstance(tc, TaskCharacteristic):
      return tc
    else:
      self.close()
      raise MalformedJSONHTTPError()

  def convert_tcrs(self,real_tc=None,fake_tc=None):
    if real_tc is not None:
      assert isinstance(real_tc,TaskCharacteristic)
      tcr_list = []
      if len(real_tc.theGrounds) > 0:
        for real_tcr in real_tc.theGrounds:
          tcr_list.append(CharacteristicReference(real_tcr[0],'grounds',real_tcr[1],real_tcr[2]))
        real_tc.theGrounds = tcr_list
        tcr_list = []
        for real_tcr in real_tc.theWarrant:
          tcr_list.append(CharacteristicReference(real_tcr[0],'warrant',real_tcr[1],real_tcr[2]))
        real_tc.theWarrant = tcr_list
        tcr_list = []
        for real_tcr in real_tc.theRebuttal:
          tcr_list.append(CharacteristicReference(real_tcr[0],'rebuttal',real_tcr[1],real_tcr[2]))
        real_tc.theRebuttal = tcr_list
      return real_tc 
    elif fake_tc is not None:
      tcr_list = []
      if len(fake_tc.theGrounds) > 0:
        for tcr in fake_tc.theGrounds:
          tcr_list.append((tcr['theReferenceName'],tcr['theReferenceDescription'],tcr['theDimensionName']))
        fake_tc.theGrounds = tcr_list
      if len(fake_tc.theWarrant) > 0:
        tcr_list = []
        for tcr in fake_tc.theWarrant:
          tcr_list.append((tcr['theReferenceName'],tcr['theReferenceDescription'],tcr['theDimensionName']))
        fake_tc.theWarrant = tcr_list
      if len(fake_tc.theRebuttal) > 0:
        tcr_list = []
        for tcr in fake_tc.theRebuttal:
          tcr_list.append((tcr['theReferenceName'],tcr['theReferenceDescription'],tcr['theDimensionName']))
        fake_tc.theRebuttal = tcr_list
      return fake_tc
