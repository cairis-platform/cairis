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
from numpy.core.multiarray import array
from cairis.core.ARM import *
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.Threat import Threat
from cairis.core.ThreatEnvironmentProperties import ThreatEnvironmentProperties
from cairis.core.ThreatParameters import ThreatParameters
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import ThreatModel, ThreatEnvironmentPropertiesModel, ThreatModelPropertyModel, ThreatModelElementModel, ThreatModelModel
from cairis.tools.PseudoClasses import SecurityAttribute
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin, Shamal Faily'


class ThreatDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)
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
      threats = self.db_proxy.getThreats(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

    threatKeys = sorted(threats.keys())
    threatList = []
    for key in threatKeys:
      threatList.append(self.simplify(threats[key]))
    return threatList

  def get_objects_summary(self):
    try:
      thrs = self.db_proxy.getThreatsSummary()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return thrs

  def get_object_by_name(self, name, simplify=True):
    found_threat = None
    try:
      threats = self.db_proxy.getThreats()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if threats is not None:
      found_threat = threats.get(name)

    if found_threat is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided threat name')

    if simplify:
      found_threat = self.simplify(found_threat)

    return found_threat
    
  def add_object(self, threat):
    threat_params = ThreatParameters(
      threatName=threat.theThreatName,
      thrType=threat.theType,
      thrMethod=threat.theMethod,
      tags=threat.theTags,
      cProperties=threat.theEnvironmentProperties
    )

    try:
      if not self.check_existing_threat(threat.theThreatName):
        self.db_proxy.addThreat(threat_params)
      else:
        raise OverwriteNotAllowedHTTPError(obj_name=threat.theThreatName)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, threat, name):
    threat_params = ThreatParameters(
      threatName=threat.theThreatName,
      thrType=threat.theType,
      thrMethod=threat.theMethod,
      tags=threat.theTags,
      cProperties=threat.theEnvironmentProperties
    )
    try:
      threatId = self.db_proxy.getDimensionId(name,'threat')
      threat_params.setId(threatId)
      self.db_proxy.updateThreat(threat_params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      threatId = self.db_proxy.getDimensionId(name,'threat')
      self.db_proxy.deleteThreat(threatId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_threat_types(self, environment_name=''):
    try:
      threat_types = self.db_proxy.getValueTypes('threat_type', environment_name)
      return threat_types
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_threat_type_by_name(self, name, environment_name=''):
    found_type = None
    threat_types = self.get_threat_types(environment_name=environment_name)

    if threat_types is None or len(threat_types) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Threat types')

    idx = 0
    while found_type is None and idx < len(threat_types):
      if threat_types[idx].theName == name:
        found_type = threat_types[idx]
      idx += 1

    if found_type is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided threat type name')

    return found_type

  def add_threat_type(self, threat_type, environment_name=''):
    assert isinstance(threat_type, ValueType)
    type_exists = self.check_existing_threat_type(threat_type.theName, environment_name=environment_name)

    if type_exists:
      self.close()
      raise OverwriteNotAllowedHTTPError(obj_name='The threat type')

    params = ValueTypeParameters(
      vtName=threat_type.theName,
      vtDesc=threat_type.theDescription,
      vType='threat_type',
      envName=environment_name,
      vtScore=threat_type.theScore,
      vtRat=threat_type.theRationale
    )

    try:
      self.db_proxy.addValueType(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_threat_type(self, threat_type, name, environment_name=''):
    assert isinstance(threat_type, ValueType)

    found_type = self.get_threat_type_by_name(name, environment_name)

    params = ValueTypeParameters(
      vtName=threat_type.theName,
      vtDesc=threat_type.theDescription,
      vType='threat_type',
      envName=environment_name,
      vtScore=threat_type.theScore,
      vtRat=threat_type.theRationale
    )
    params.setId(found_type.theId)

    try:
      self.db_proxy.updateValueType(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_threat_type(self, name, environment_name=''):
    found_type = self.get_threat_type_by_name(name, environment_name)

    try:
      self.db_proxy.deleteThreatType(found_type.theId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def buildThreatModelElement(self,elements):

    apDict = {}
    for ap in elements:
      if ap[0] not in apDict:
        propDict = {'Confidentiality':[],'Integrity':[],'Availability':[],'Accountability':[],'Anonymity':[],'Pseudonymity':[],'Unlinkability':[],'Unobservability':[]}
        apDict[ap[0]] = propDict
      apDict[ap[0]][ap[2]].append(ap[1])
    els = []
    for ap in apDict:
      elObjt = ThreatModelElementModel()
      elObjt.theElement = ap
      elObjt.theProperties = []
      props = ['Confidentiality','Integrity','Availability','Accountability','Anonymity','Pseudonymity','Unlinkability','Unobservability']
      for prop in props:
        propObjt = ThreatModelPropertyModel()
        propObjt.theProperty = prop
        propObjt.theThreats = apDict[ap][prop]
        elObjt.theProperties.append(propObjt)
      els.append(elObjt)
    return els


  def get_threat_model(self,environment_name):
    try:
      tm = ThreatModelModel()
      tm.theEntities = self.buildThreatModelElement(self.db_proxy.threatenedEntities(environment_name))
      tm.theProcesses = self.buildThreatModelElement(self.db_proxy.threatenedProcesses(environment_name))
      tm.theDatastores = self.buildThreatModelElement(self.db_proxy.threatenedDatastores(environment_name))
      tm.theDataflows = self.buildThreatModelElement(self.db_proxy.threatenedDataflows(environment_name))
      return tm
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_threat(self, name):
    try:
      self.db_proxy.nameCheck(name, 'threat')
      return False
    except ARMException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_threat_type(self, name, environment_name):
    try:
      self.get_threat_type_by_name(name, environment_name)
      return True
    except ObjectNotFoundHTTPError:
      self.db_proxy.reconnect(session_id=self.session_id)
      return False
    
  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, ThreatModel.required)
    json_dict['__python_obj__'] = Threat.__module__+'.'+Threat.__name__

    threat_props = self.convert_props(fake_props=json_dict['theEnvironmentProperties'])
    json_dict['theEnvironmentProperties'] = []

    threat = json_serialize(json_dict)
    threat = json_deserialize(threat)
    threat.theEnvironmentProperties = threat_props
    if not isinstance(threat, Threat):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return threat

  def simplify(self, obj):
    assert isinstance(obj, Threat)
    del obj.theId 
    del obj.theEnvironmentDictionary
    del obj.likelihoodLookup
    del obj.theThreatPropertyDictionary
    obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties)
    return obj

  def convert_props(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      if len(real_props) > 0:
        assert isinstance(real_props[0], ThreatEnvironmentProperties)
        for real_prop in real_props:
          assert isinstance(real_prop, ThreatEnvironmentProperties)
          assert len(real_prop.theProperties) == len(real_prop.theRationale)
          new_attrs = []
          for idx in range(0, len(real_prop.theProperties)):
            attr_name = self.rev_attr_dict.get(idx)
            attr_value = self.prop_dict[real_prop.theProperties[idx]]
            attr_rationale = real_prop.theRationale[idx]
            new_attr = SecurityAttribute(attr_name, attr_value, attr_rationale)
            new_attrs.append(new_attr)
          real_prop.theProperties = new_attrs
          del real_prop.theRationale
          new_props.append(real_prop)

      return new_props
    elif fake_props is not None:
      if len(fake_props) > 0:
        check_required_keys(fake_props[0], ThreatEnvironmentPropertiesModel.required)
        for fake_prop in fake_props:
          check_required_keys(fake_prop, ThreatEnvironmentPropertiesModel.required)
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
          new_prop = ThreatEnvironmentProperties(
            environmentName=fake_prop['theEnvironmentName'],
            lhood=fake_prop['theLikelihood'],
            assets=fake_prop['theAssets'],
            attackers=fake_prop['theAttackers'],
            pRationale=fake_prop['theRationale'],
            syProperties=fake_prop['theProperties']
          )
          new_props.append(new_prop)

      return new_props
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])
