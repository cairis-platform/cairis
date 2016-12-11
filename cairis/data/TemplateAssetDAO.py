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
    self.rev_value_dict = {0:'None', 1:'Low',2:'Medium', 3:'High'}


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
        return tas[key]
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
      spRationale=ta.theRationale,
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
      spRationale=ta.theRationale,
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
    ifs = json_dict.pop('theInterfaces',[])
    ifs = self.convert_ifs(fake_ifs=ifs)

    ta = json_serialize(json_dict)
    ta = json_deserialize(ta)

    if isinstance(ta, TemplateAsset):
      ta.theInterfaces = ifs
      return ta
    else:
      self.close()
      raise MalformedJSONHTTPError()

  def simplify(self, ta):
    assert isinstance(ta, TemplateAsset)
    ta.theInterfaces = self.convert_ifs(real_ifs=ta.theInterfaces)
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
