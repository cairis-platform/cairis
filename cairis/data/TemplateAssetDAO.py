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

import numpy
from numpy.core.multiarray import array
from cairis.core.ARM import *
from cairis.core.TemplateAsset import TemplateAsset
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import TemplateAssetModel, SecurityAttribute
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class TemplateAssetDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'template_asset')
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
    self.rev_attr_dict = {}
    for key, value in list(self.attr_dict.items()):
      self.rev_attr_dict[value] = key
    self.rev_value_dict = {0:'None', 1:'Low',2:'Medium', 3:'High'}


  def get_objects(self,constraint_id = -1):
    try:
      tas = self.db_proxy.getTemplateAssets(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    tasList = []
    for key, value in list(tas.items()):
      tasList.append(self.simplify(value))
    return tasList

  def get_object_by_name(self, template_asset_name):
    try:
      found_ta = None
      taId = self.db_proxy.getDimensionId(template_asset_name,'template_asset')
      tas = self.db_proxy.getTemplateAssets(taId)
      if tas is not None:
        found_ta = tas.get(template_asset_name)
      if found_ta is None:
        self.close()
        raise ObjectNotFoundHTTPError('The provided template asset')
      return self.simplify(found_ta)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided template asset')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, ta):
    taParams = TemplateAssetParameters(
      assetName=ta.theName,
      shortCode=ta.theShortCode,
      assetDesc=ta.theDescription,
      assetSig=ta.theSignificance,
      assetType=ta.theType,
      sType=ta.theSurfaceType,
      aRight=ta.theAccessRight,
      spValues=ta.theProperties,
      spRationale=ta.theRationale,
      tags=ta.theTags,
      ifs=ta.theInterfaces)
    try:
      self.db_proxy.addTemplateAsset(taParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self,ta,name):
    taParams = TemplateAssetParameters(
      assetName=ta.theName,
      shortCode=ta.theShortCode,
      assetDesc=ta.theDescription,
      assetSig=ta.theSignificance,
      assetType=ta.theType,
      sType=ta.theSurfaceType,
      aRight=ta.theAccessRight,
      spValues=ta.theProperties,
      spRationale=ta.theRationale,
      tags=ta.theTags,
      ifs=ta.theInterfaces)
    try:
      taId = self.db_proxy.getDimensionId(name,'template_asset')
      taParams.setId(taId)
      self.db_proxy.updateTemplateAsset(taParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      taId = self.db_proxy.getDimensionId(name,'template_asset')
      self.db_proxy.deleteTemplateAsset(taId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, TemplateAssetModel.required)
    json_dict['__python_obj__'] = TemplateAsset.__module__+'.'+ TemplateAsset.__name__
    ifs = json_dict.pop('theInterfaces',[])
    ifs = self.convert_ifs(fake_ifs=ifs)
    props = json_dict.pop('theProperties',[])
    ta = json_serialize(json_dict)
    props,rats = self.convert_props(fake_props=props)
    ta = json_deserialize(ta)

    if isinstance(ta, TemplateAsset):
      ta.theInterfaces = ifs
      ta.theProperties = props
      ta.theRationale = rats
      return ta
    else:
      self.close()
      raise MalformedJSONHTTPError()

  def simplify(self, ta):
    assert isinstance(ta, TemplateAsset)
    del ta.theId
    ta.theInterfaces = self.convert_ifs(real_ifs=ta.theInterfaces)
    ta.theProperties = self.convert_props(real_props=ta.theProperties,fake_props=None,rationales=ta.theRationale)
    del ta.theRationale
    return ta

  def convert_ifs(self, real_ifs=None, fake_ifs=None):
    new_ifs = []
    if real_ifs is not None:
      if len(real_ifs) > 0:
        for rIf in real_ifs:
          ifDict = {}
          ifDict['theInterfaceName'] = rIf[0]
          ifDict['theInterfaceType'] = rIf[1]
          ifDict['theAccessRight'] = rIf[2]
          ifDict['thePrivilege'] = rIf[3]
          new_ifs.append(ifDict)
    elif fake_ifs is not None:
      if len(fake_ifs) > 0:
        for fIf in fake_ifs:
          new_ifs.append((fIf['theInterfaceName'],fIf['theInterfaceType'],fIf['theAccessRight'],fIf['thePrivilege']))
    return new_ifs


  def convert_props(self, real_props=None, fake_props=None, rationales=None):
    prop_dict = {}
    prop_dict['None'] = 0
    prop_dict['Low'] = 1
    prop_dict['Medium'] = 2
    prop_dict['High'] = 3
    rev_prop_dict = {}
    rev_prop_dict[0] = 'None'
    rev_prop_dict[1] = 'Low'
    rev_prop_dict[2] = 'Medium'
    rev_prop_dict[3] = 'High'
    new_props = []
    if real_props is not None:
      if len(real_props) > 0:
        new_sec_attrs = []
        for idx in range(0, len(real_props)):
          try:
            attr_name = self.rev_attr_dict[idx]
            attr_value = rev_prop_dict[real_props[idx]]
            new_sec_attr = SecurityAttribute(attr_name, attr_value, rationales[idx])
            new_props.append(new_sec_attr)
          except LookupError:
            self.logger.warning('Unable to find key in dictionary. Attribute is being skipped.')
      return new_props
    elif fake_props is not None:
      if len(fake_props) > 0:
        new_props = array(8 * [0]).astype(numpy.int32)
        new_rationale = ['None'] * 8
        for sec_attr in fake_props:
          attr_id = self.attr_dict[sec_attr['name']]
          attr_value = prop_dict[sec_attr['value']]
          attr_rationale = sec_attr['rationale']
          new_props[attr_id] = attr_value
          new_rationale[attr_id] = attr_rationale
      return (new_props,new_rationale)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])

