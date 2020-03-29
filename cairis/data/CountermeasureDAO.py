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

import numpy.core
import cairis.core.AssetParametersFactory
from numpy.core.multiarray import array
from cairis.core.ARM import *
from cairis.core.CountermeasureEnvironmentProperties import CountermeasureEnvironmentProperties
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.Countermeasure import Countermeasure
from cairis.core.CountermeasureParameters import CountermeasureParameters
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
import cairis.core.armid
from cairis.misc.KaosModel import KaosModel
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import CountermeasureModel, CountermeasureEnvironmentPropertiesModel,CountermeasureTask
from cairis.tools.PseudoClasses import SecurityAttribute, CountermeasureTarget, CountermeasureTaskCharacteristics
from cairis.tools.SessionValidator import check_required_keys, get_fonts

__author__ = 'Shamal Faily'


class CountermeasureDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'countermeasure')
    self.prop_dict = {
      0:'None',
      1:'Low',
      2:'Medium',
      3:'High'
    }
    self.attr_dict = {
      'Confidentiality': cairis.core.armid.C_PROPERTY,
      'Integrity': cairis.core.armid.I_PROPERTY,
      'Availability': cairis.core.armid.AV_PROPERTY,
      'Accountability': cairis.core.armid.AC_PROPERTY,
      'Anonymity': cairis.core.armid.AN_PROPERTY,
      'Pseudonymity': cairis.core.armid.PAN_PROPERTY,
      'Unlinkability': cairis.core.armid.UNL_PROPERTY,
      'Unobservability': cairis.core.armid.UNO_PROPERTY
    }
    self.rev_attr_dict = dict()
    self.rev_prop_dict = dict()
    for key, value in list(self.attr_dict.items()):
      self.rev_attr_dict[value] = key
    for key, value in list(self.prop_dict.items()):
      self.rev_prop_dict[value] = key


  def get_objects(self, constraint_id=-1):
    try:
      countermeasures = self.db_proxy.getCountermeasures(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    cmKeys = sorted(countermeasures.keys())
    cmList = []
    for key in cmKeys:
      value = countermeasures[key]
      cmList.append(self.simplify(value))
    return cmList

  def get_object_by_name(self, name):
    try:
      cmId = self.db_proxy.getDimensionId(name,'countermeasure')
      countermeasures = self.get_objects(cmId)
      return countermeasures[0]
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided countermeasure name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)



  def add_object(self, countermeasure):
    countermeasure_params = CountermeasureParameters(
      cmName=countermeasure.name(),
      cmDesc=countermeasure.description(),
      cmType=countermeasure.type(),
      tags=countermeasure.tags(),
      cProps=countermeasure.environmentProperties()
    )

    try:
      if not self.check_existing_countermeasure(countermeasure.name()):
        self.db_proxy.addCountermeasure(countermeasure_params)
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=countermeasure.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, countermeasure, name):
    countermeasure_params = CountermeasureParameters(
      cmName=countermeasure.name(),
      cmDesc=countermeasure.description(),
      cmType=countermeasure.type(),
      tags=countermeasure.tags(),
      cProps=countermeasure.environmentProperties()
    )

    try:
      cmId = self.db_proxy.getDimensionId(name,'countermeasure')
      countermeasure_params.setId(cmId)
      self.db_proxy.updateCountermeasure(countermeasure_params)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided countermeasure name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      cmId = self.db_proxy.getDimensionId(name,'countermeasure')
      self.db_proxy.deleteCountermeasure(cmId)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided countermeasure name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_countermeasure(self, name):
    try:
      self.db_proxy.nameCheck(name, 'countermeasure')
      return False
    except DatabaseProxyException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
        self.close()
        raise ARMHTTPError(ex)
    except ARMException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
        self.close()
        raise ARMHTTPError(ex)

  def get_countermeasure_targets(self,envName,pathValues):
    reqList = pathValues[0]
    try:
      return list(self.db_proxy.targetNames(reqList,envName).keys())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_countermeasure_tasks(self,envName,pathValues):
    roleList = pathValues[0]
    try:
      roleTasks = self.db_proxy.roleTasks(envName,roleList)
      outRoleTasks = []
      for key in roleTasks:
        taskData = roleTasks[key]
        outRoleTasks.append(CountermeasureTask(key[1],key[0],taskData[0],taskData[1],taskData[2],taskData[3]))
      return outRoleTasks
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def generate_asset(self,cmName,pathValues = []):
    try:
      cm = self.db_proxy.dimensionObject(cmName,'countermeasure')
      assetParameters = cairis.core.AssetParametersFactory.build(cm,self.db_proxy)
      self.db_proxy.nameCheck(assetParameters.name(),'asset')
      assetId = self.db_proxy.addAsset(assetParameters)
      self.db_proxy.addTrace('countermeasure_asset',cm.id(),assetId)
      return 'Asset ' + cmName + ' CM created'
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided countermeasure name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def generate_asset_from_template(self,cmName,taName,pathValues = []):
    try:
      cm = self.db_proxy.dimensionObject(cmName,'countermeasure')
      taParameters = cairis.core.AssetParametersFactory.buildFromTemplate(taName,cm.environments())
      self.db_proxy.nameCheck(taParameters.name(),'asset')
      assetId = self.db_proxy.addAsset(taParameters)
      self.db_proxy.addTrace('countermeasure_asset',cm.id(),assetId)
      return 'Asset ' + taName + ' created'
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided countermeasure name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def situate_countermeasure_pattern(self,cmName,spName,pathValues = []):
    try:
      cm = self.db_proxy.dimensionObject(cmName,'countermeasure')
      patternId = self.db_proxy.getDimensionId(spName,'securitypattern')
      assetParametersList = []
      for assetName in self.db_proxy.patternAssets(patternId):
        taParameters = cairis.core.AssetParametersFactory.buildFromTemplate(assetName,cm.environments())
        assetParametersList.append(taParameters)
      self.db_proxy.addSituatedAssets(patternId,assetParametersList)
      self.db_proxy.addTrace('countermeasure_securitypattern',cm.id(),patternId)
      return spName + ' situated'
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided countermeasure name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def associate_situated_pattern(self,cmName,spName, pathValues = []):
    try:
      cmId = self.db_proxy.getDimensionId(cmName,'countermeasure')
      self.db_proxy.associateCountermeasureToPattern(cmId,spName)
      return spName + ' associated'
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided countermeasure name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def remove_situated_pattern(self,cmName,spName, pathValues = []):
    try:
      cmId = self.db_proxy.getDimensionId(cmName,'countermeasure')
      self.db_proxy.deleteSituatedPattern(cmId,spName)
      return 'Situated pattern ' + spName + ' removed'
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided countermeasure name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def candidate_countermeasure_patterns(self,cmName, pathValue = []):
    try:
      cmId = self.db_proxy.getDimensionId(cmName,'countermeasure')
      return self.db_proxy.candidateCountermeasurePatterns(cmId)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided countermeasure name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def countermeasure_patterns(self,cmName, pathValues = []):
    try:
      cmId = self.db_proxy.getDimensionId(cmName,'countermeasure')
      return self.db_proxy.countermeasurePatterns(cmId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, CountermeasureModel.required)
    json_dict['__python_obj__'] = Countermeasure.__module__ + '.' + Countermeasure.__name__

    countermeasure_props = self.convert_props(fake_props=json_dict['theEnvironmentProperties'])
    json_dict['theEnvironmentProperties'] = []

    countermeasure = json_serialize(json_dict)
    countermeasure = json_deserialize(countermeasure)
    countermeasure.theEnvironmentProperties = countermeasure_props
    if not isinstance(countermeasure, Countermeasure):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return countermeasure

  def simplify(self, obj):
    assert isinstance(obj, Countermeasure)
    del obj.theId
    del obj.theEnvironmentDictionary
    del obj.theCountermeasurePropertyDictionary
    del obj.costLookup
    del obj.effectivenessLookup
    obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties)
    return obj

  def convert_props(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      if len(real_props) > 0:
        for real_prop in real_props:
          assert isinstance(real_prop, CountermeasureEnvironmentProperties)
          ctList = []
          for ctc in real_prop.personas():
            ctList.append(CountermeasureTaskCharacteristics(ctc[0],ctc[1],ctc[2],ctc[3],ctc[4],ctc[5]))
          real_prop.thePersonas = ctList
          assert len(real_prop.theProperties) == len(real_prop.theRationale)
          new_attrs = []
          for idx in range(0, len(real_prop.theProperties)):
            attr_name = self.rev_attr_dict.get(idx)
            attr_value = self.prop_dict[real_prop.theProperties[idx]]
            attr_rationale = real_prop.theRationale[idx]
            new_attr = SecurityAttribute(attr_name, attr_value, attr_rationale)
            new_attrs.append(new_attr)
          real_prop.theProperties = new_attrs
          new_targets = []
          for idx in range(0, len(real_prop.theTargets)):
            tName = real_prop.theTargets[idx][0]
            tEff = real_prop.theTargets[idx][1]
            tRat = real_prop.theTargets[idx][2]
            new_targets.append(CountermeasureTarget(tName,tEff,tRat))
          real_prop.theTargets = new_targets
          del real_prop.theRationale
          new_props.append(real_prop)
      return new_props
    elif fake_props is not None:
      if len(fake_props) > 0:
        for fake_prop in fake_props:
          check_required_keys(fake_prop, CountermeasureEnvironmentPropertiesModel.required)
          ctList = []
          for ctc in fake_prop['thePersonas']:
            ctList.append([ctc['theTask'],ctc['thePersona'],ctc['theDuration'],ctc['theFrequency'],ctc['theDemands'],ctc['theGoalConflict']])
          fake_prop['thePersonas'] = ctList
          new_ndprops = array([0]*8).astype(numpy.core.int32)
          new_ratios = ['None']*8
          for idx in range(0, len(fake_prop['theProperties'])):
            new_attr = fake_prop['theProperties'][idx]
            check_required_keys(new_attr, SecurityAttribute.required)
            attr_id = self.attr_dict.get(new_attr['name'], -1)
            if -1 < attr_id < len(self.attr_dict):
              attr_value = self.rev_prop_dict[new_attr['value']]
              attr_rationale = new_attr['rationale']
              new_ndprops[attr_id] = attr_value
              new_ratios[attr_id] = attr_rationale
          fake_prop['theProperties'] = new_ndprops
          fake_prop['theRationale'] = new_ratios
          new_targets = []
          for idx in range(0, len(fake_prop['theTargets'])):
            tName = fake_prop['theTargets'][idx]['theName']
            tEff = fake_prop['theTargets'][idx]['theEffectiveness']
            tRat = fake_prop['theTargets'][idx]['theRationale']
            new_targets.append(CountermeasureTarget(tName,tEff,tRat))
          fake_prop['theTargets'] = new_targets
          check_required_keys(fake_prop, CountermeasureEnvironmentPropertiesModel.required)
          new_prop = CountermeasureEnvironmentProperties(
                       environmentName=fake_prop['theEnvironmentName'],
                       requirements=fake_prop['theRequirements'],
                       targets=fake_prop['theTargets'],
                       properties=fake_prop['theProperties'],
                       rationale=fake_prop['theRationale'],
                       cost=fake_prop['theCost'],
                       roles=fake_prop['theRoles'],
                       personas=fake_prop['thePersonas']
                     )
          new_props.append(new_prop)
      return new_props
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])
