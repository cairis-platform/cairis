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
    CairisDAO.__init__(self, session_id)
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
    for key, value in self.attr_dict.items():
      self.rev_attr_dict[value] = key


  def get_template_assets(self,constraint_id = -1):
    """
    :rtype: dict[str,TemplateAsset]
    :return
    :raise ARMHTTPError:
    """
    try:
      tas = self.db_proxy.getTemplateAssets(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    for key, value in tas.items():
      tas[key] = self.simplify(value)
    return tas

  def get_template_asset(self, template_asset_name):
    tas = self.get_template_assets()
    if tas is None or len(tas) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Template Assets')
    for key in tas:
      if (key == template_asset_name):
        ta = self.simplify(tas[key])
        return ta
    self.close()
    raise ObjectNotFoundHTTPError('The provided template asset parameters')

  def add_template_asset(self, ta):
    taParams = TemplateAssetParameters(
      assetName=ta.theName,
      shortCode=ta.theShortCode,
      assetDesc=ta.theDescription,
      assetSig=ta.theSignificance,
      assetType=ta.theType,
      sType=ta.theSurfaceType,
      aRight=ta.theAccessRight,
      spValues=ta.theProperties,
      tags=ta.theTags,
      ifs=ta.theInterfaces)
    try:
      self.db_proxy.addTemplateAsset(taParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_template_asset(self,ta,name):
    found_ta = self.get_template_asset(name)
    taParams = TemplateAssetParameters(
      assetName=ta.theName,
      shortCode=ta.theShortCode,
      assetDesc=ta.theDescription,
      assetSig=ta.theSignificance,
      assetType=ta.theType,
      sType=ta.theSurfaceType,
      aRight=ta.theAccessRight,
      spValues=ta.theProperties,
      tags=ta.theTags,
      ifs=ta.theInterfaces)
    taParams.setId(found_ta.theId)
    try:
      self.db_proxy.updateTemplateAsset(taParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_template_asset(self, name):
    ta = self.get_template_asset(name)
    try:
      self.db_proxy.deleteTemplateAsset(ta.theId)
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
    ta = json_serialize(json_dict)
    ta = json_deserialize(ta)

    if isinstance(ta, TemplateAsset):
      return ta
    else:
      self.close()
      raise MalformedJSONHTTPError()

  def simplify(self, ta):
    assert isinstance(ta, TemplateAsset)
    ta.theInterfaces = self.convert_ifs(real_ifs=ta.theInterfaces)
    secProps = self.convert_props(real_props=ta.theProperties)
    ta.theConfidentialityProperty = secProps[self.attr_dict['Confidentiality']].value
    ta.theConfidentialityRationale = secProps[self.attr_dict['Confidentiality']].rationale
    ta.theIntegrityProperty = secProps[self.attr_dict['Integrity']].value
    ta.theIntegrityRationale = secProps[self.attr_dict['Integrity']].rationale
    ta.theAvailabilityProperty = secProps[self.attr_dict['Availability']].value
    ta.theAvailabilityRationale = secProps[self.attr_dict['Availability']].rationale
    ta.theAccountabilityProperty = secProps[self.attr_dict['Accountability']].value
    ta.theAccountabilityRationale = secProps[self.attr_dict['Accountability']].rationale
    ta.theAnonymityProperty = secProps[self.attr_dict['Anonymity']].value
    ta.theAnonymityRationale = secProps[self.attr_dict['Anonymity']].rationale
    ta.thePseudonymityProperty = secProps[self.attr_dict['Pseudonymity']].value
    ta.thePseudonymityRationale = secProps[self.attr_dict['Pseudonymity']].rationale
    ta.theUnlinkabilityProperty = secProps[self.attr_dict['Unlinkability']].value
    ta.theUnlinkabilityRationale = secProps[self.attr_dict['Unlinkability']].rationale
    ta.theUnobservabilityProperty = secProps[self.attr_dict['Unobservability']].value
    ta.theUnobservabilityRationale = secProps[self.attr_dict['Unobservability']].rationale
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

  def convert_props(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      for idx in range(0, len(real_props)):
        try:
          attr_name = self.rev_attr_dict[idx]
          attr_value = real_props[idx][0]
          new_sec_attr = SecurityAttribute(attr_name, attr_value, real_props[idx][1])
          new_props.append(new_sec_attr)
        except LookupError:
          self.logger.warning('Unable to find key in dictionary. Attribute is being skipped.')
    elif fake_props is not None:
      sec_attrs = fake_prop['theProperties']
      new_syProps = array(8 * [0]).astype(numpy.int32)
      new_rationale = ['None'] * 8

      for sec_attr in sec_attrs:
        attr_id = self.attr_dict[sec_attr['name']]
        attr_value = rev_prop_dict[sec_attr['value']]
        attr_rationale = sec_attr['rationale']
        new_syProps[attr_id] = attr_value
        new_rationale[attr_id] = attr_rationale
      new_props.append(new_syProps)
      new_props.append(new_rationale)
    return new_props
