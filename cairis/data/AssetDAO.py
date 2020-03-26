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
from cairis.core.Asset import Asset
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.AssetParameters import AssetParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import AssetEnvironmentPropertiesModel, SecurityAttribute, AssetModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.misc.AssetModel import AssetModel as GraphicalAssetModel

__author__ = 'Robin Quetin, Shamal Faily'


class AssetDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'asset')
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

  def get_objects(self, constraint_id=-1, simplify=True):
    try:
      assets = self.db_proxy.getAssets(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    if simplify:
      assetList = []
      for key, value in list(assets.items()):
        assetList.append(self.simplify(value))
    return assetList

  def get_objects_summary(self):
    try:
      assets = self.db_proxy.getAssetsSummary()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return assets

  def get_asset_names_by_environment(self, environment, pathValues = []):
    return self.get_asset_names([environment])

  def get_asset_names(self, pathValues):
    try:
      environment = pathValues[0]
      asset_names = self.db_proxy.getDimensionNames('asset', environment)
      return asset_names
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_object_by_name(self, name):
    try:
      assetId = self.db_proxy.getDimensionId(name,'asset')
      assets = self.db_proxy.getAssets(assetId)
      return self.simplify(assets.get(name))
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided asset name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_threatened_assets(self, threat_name, environment_name):
    try:
      threat_id = self.db_proxy.getDimensionId(threat_name,'threat')
      environment_id = self.db_proxy.getDimensionId(environment_name,'environment')
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError(ex)
    except ObjectNotFoundHTTPError as ex:
      self.close()
      raise ex
    except ARMHTTPError as ex:
      self.close()
      raise ex

    try:
      threatened_assets = self.db_proxy.threatenedAssets(threat_id, environment_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    return threatened_assets

  def get_vulnerable_assets(self, vulnerability_name, environment_name):
    try:
      vulnerability_id = self.db_proxy.getDimensionId(vulnerability_name,'vulnerability')
      environment_id = self.db_proxy.getDimensionId(environment_name,'environment')
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError(ex)
    except ObjectNotFoundHTTPError as ex:
      self.close()
      raise ex
    except ARMHTTPError as ex:
      self.close()
      raise ex

    try:
      vulnerable_assets = self.db_proxy.vulnerableAssets(vulnerability_id, environment_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    return vulnerable_assets

  def add_object(self, asset, asset_props=None):
    try:
      self.db_proxy.nameCheck(asset.theName, 'asset')
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    assetParams = AssetParameters(
      assetName=asset.theName,
      shortCode=asset.theShortCode,
      assetDesc=asset.theDescription,
      assetSig=asset.theSignificance,
      assetType=asset.theType,
      cFlag=asset.isCritical,
      cRationale=asset.theCriticalRationale,
      tags=asset.theTags,
      ifs=asset.theInterfaces,
      cProperties=asset.theEnvironmentProperties
    )

    self.db_proxy.addAsset(assetParams)
    return asset.theName

  def update_object(self, asset, name):
    params = AssetParameters(
      assetName=asset.theName,
      shortCode=asset.theShortCode,
      assetDesc=asset.theDescription,
      assetSig=asset.theSignificance,
      assetType=asset.theType,
      cFlag=asset.isCritical,
      cRationale=asset.theCriticalRationale,
      tags=asset.theTags,
      ifs=asset.theInterfaces,
      cProperties=asset.theEnvironmentProperties
    )

    try:
      assetId = self.db_proxy.getDimensionId(name,'asset')
      params.setId(assetId)
      self.db_proxy.updateAsset(params)
      return asset.theName
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError(ex)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      assetId = self.db_proxy.getDimensionId(name,'asset')
      self.db_proxy.deleteAsset(assetId)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError(ex)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_asset_model(self, environment_name, asset_name, pathValues):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)

    hide_concerns = pathValues[0]
    if hide_concerns == '0' or hide_concerns == 0:
      hide_concerns = False
    else:
      hide_concerns = True

    if asset_name == 'all':
      asset_name = ''

    try:
      self.db_proxy.getDimensionId(environment_name,'environment')
      if (asset_name != ''):
        self.db_proxy.getDimensionId(asset_name,'asset')

      associationDictionary = self.db_proxy.classModel(environment_name, asset_name, hideConcerns=hide_concerns)
      associations = GraphicalAssetModel(list(associationDictionary.values()), environment_name, asset_name, hideConcerns=hide_concerns, db_proxy=self.db_proxy, fontName=fontName, fontSize=fontSize)
      dot_code = associations.graph()
      return dot_code
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError(ex)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except Exception as ex:
      print(ex)

  def get_asset_types(self, pathValues):
    try:
      environment_name = pathValues[0]
      asset_types = self.db_proxy.getValueTypes('asset_type', environment_name)
      return asset_types
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_asset_type_by_name(self, name, pathValues):
    found_type = None
    asset_types = self.get_asset_types(pathValues)

    if asset_types is None or len(asset_types) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Asset types')

    idx = 0
    while found_type is None and idx < len(asset_types):
      if asset_types[idx].theName == name:
        found_type = asset_types[idx]
      idx += 1

    if found_type is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided asset type name')

    return found_type

  def add_asset_type(self, asset_type, pathValues):
    assert isinstance(asset_type, ValueType)
    environment_name = pathValues[0]
    type_exists = self.check_existing_asset_type(asset_type.theName, environment_name=environment_name)

    if type_exists:
      self.close()
      raise OverwriteNotAllowedHTTPError(obj_name='The asset type')

    params = ValueTypeParameters(
      vtName=asset_type.theName,
      vtDesc=asset_type.theDescription,
      vType='asset_type',
      envName=environment_name,
      vtScore=asset_type.theScore,
      vtRat=asset_type.theRationale
    )

    try:
      self.db_proxy.addValueType(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_asset_type(self, asset_type, name, pathValues):
    assert isinstance(asset_type, ValueType)
    found_type = self.get_asset_type_by_name(name, pathValues)
    environment_name = pathValues[0]

    params = ValueTypeParameters(
      vtName=asset_type.theName,
      vtDesc=asset_type.theDescription,
      vType='asset_type',
      envName=environment_name,
      vtScore=asset_type.theScore,
      vtRat=asset_type.theRationale
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

  def delete_asset_type(self, name, pathValues):
    environment_name = pathValues[0]
    found_type = self.get_asset_type_by_name(name, pathValues)

    try:
      self.db_proxy.deleteAssetType(found_type.theId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_asset_type(self, name, environment_name):
    try:
      self.get_asset_type_by_name(name, [environment_name])
      return True
    except ObjectNotFoundHTTPError:
      self.db_proxy.reconnect(session_id=self.session_id)
      return False

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
      if len(real_props) > 0:
        for real_prop in real_props:
          assert isinstance(real_prop, AssetEnvironmentProperties)
          asset_values = self.db_proxy.getValueTypes('asset_value', real_prop.theEnvironmentName)
          prop_dict = {}
          for asset_value in asset_values:
            prop_dict[asset_value.theId] = asset_value.theName

          for idx in range(0, len(real_prop.theAssociations)):
            realAssoc = real_prop.theAssociations[idx]
            fakeAssoc = {'theHeadNav':realAssoc[0],'theHeadType':realAssoc[1],'theHeadMultiplicity':realAssoc[2],'theHeadRole':realAssoc[3],'theTailRole':realAssoc[4],'theTailMultiplicity':realAssoc[5],'theTailType':realAssoc[6],'theTailNav':realAssoc[7],'theTailName':realAssoc[8]}
            real_prop.theAssociations[idx] = fakeAssoc
          sec_props = real_prop.theProperties
          rationales = real_prop.theRationale

          if len(sec_props) == len(rationales):
            new_sec_attrs = []
            for idx in range(0, len(sec_props)):
              try:
                attr_name = self.rev_attr_dict[idx]
                attr_value = prop_dict[sec_props[idx]]
                new_sec_attr = SecurityAttribute(attr_name, attr_value, rationales[idx])
                new_sec_attrs.append(new_sec_attr)
              except LookupError:
                self.logger.warning('Unable to find key in dictionary. Attribute is being skipped.')
            real_prop.theProperties = new_sec_attrs
            delattr(real_prop, 'theRationale')
          new_props.append(real_prop)
    elif fake_props is not None:
      if len(fake_props) > 0:
        for fake_prop in fake_props:
          check_required_keys(fake_prop, AssetEnvironmentPropertiesModel.required)
          asset_values = self.db_proxy.getValueTypes('asset_value', fake_prop['theEnvironmentName'])
          rev_prop_dict = {}
          for asset_value in asset_values:
            rev_prop_dict[asset_value.theName] = asset_value.theId

          assert isinstance(fake_prop['theAssociations'], list)
          for idx in range(0, len(fake_prop['theAssociations'])):
            fakeAssoc = fake_prop['theAssociations'][idx] 
            fake_prop['theAssociations'][idx] = (fakeAssoc['theHeadNav'],fakeAssoc['theHeadType'],fakeAssoc['theHeadMultiplicity'],fakeAssoc['theHeadRole'],fakeAssoc['theTailRole'],fakeAssoc['theTailMultiplicity'],fakeAssoc['theTailType'],fakeAssoc['theTailNav'],fakeAssoc['theTailName'])
          sec_attrs = fake_prop['theProperties']
          new_syProps = array(8 * [0]).astype(numpy.int32)
          new_rationale = ['None'] * 8

          for sec_attr in sec_attrs:
            attr_id = self.attr_dict[sec_attr['name']]
            attr_value = rev_prop_dict[sec_attr['value']]
            attr_rationale = sec_attr['rationale']
            new_syProps[attr_id] = attr_value
            new_rationale[attr_id] = attr_rationale

          new_prop = AssetEnvironmentProperties(
            environmentName=fake_prop['theEnvironmentName'],
            syProperties=new_syProps,
            pRationale=new_rationale,
            associations=fake_prop['theAssociations']
          )
          new_props.append(new_prop)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])

    return new_props

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, AssetModel.required)
    env_props = json_dict.pop('theEnvironmentProperties', [])
    env_props = self.convert_props(fake_props=env_props)
    ifs = json_dict.pop('theInterfaces',[])
    ifs = self.convert_ifs(fake_ifs=ifs)
    json_dict.pop('theEnvironmentDictionary', None)
    json_dict.pop('theAssetPropertyDictionary', None)
    asset = json_dict
    asset['__python_obj__'] = Asset.__module__+'.'+Asset.__name__
    asset = json_deserialize(asset)

    if isinstance(asset, Asset):
      asset.theInterfaces = ifs
      asset.theEnvironmentProperties = env_props
      return asset
    else:
      self.close()
      raise MalformedJSONHTTPError()

  def simplify(self, asset):
    """
    Simplifies the Asset object by removing the environment properties
    :param asset: The Asset to simplify
    :type asset: Asset
    :return: The simplified Asset
    :rtype: Asset
    """
    assert isinstance(asset, Asset)
    del asset.theId
    asset.theInterfaces = self.convert_ifs(real_ifs=asset.theInterfaces)
    asset.theEnvironmentProperties = self.convert_props(real_props=asset.theEnvironmentProperties)
    del asset.theEnvironmentDictionary
    del asset.theAssetPropertyDictionary
    return asset

  def get_asset_association(self, environment_name, head_name, tail_name):
    assocs = self.db_proxy.classModel(environment_name)
    if assocs is None or len(assocs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Asset Associations')
    for key in assocs:
      envName,headName,tailName = key.split('/')
      if (envName == environment_name) and (((headName == head_name) and (tailName == tail_name)) or ((headName == tail_name) and (tailName == head_name))):
        assoc = assocs[key]
        self.close()
        return assoc 
    self.close()
    raise ObjectNotFoundHTTPError('The provided asset association parameters')

  def add_asset_assocition(self, assoc):
    
    assocParams = ClassAssociationParameters(
      envName=assoc.theEnvironmentName,
      headName=assoc.theHeadAsset,
      headDim='asset',
      headNav=assoc.theHeadNav,
      headType=assoc.theHeadType,
      headMultiplicity=assoc.theHeadMultiplicity,
      headRole=assoc.theHeadRole,
      tailRole=assoc.theTailRole,
      tailMultiplicity=assoc.theTailMultiplicity,
      tailType=assoc.theTailType,
      tailNav=assoc.theTailNav,
      tailDim='asset',
      tailName=assoc.theTailAsset,
      rationale=asset.theRationale)
    try:
      self.db_proxy.addClassAssociation(assocParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_asset_assocition(self, environment_name,head_name,tail_name,assoc):
    old_assoc = self.get_asset_association(environment_name,head_name,tail_name)
    id = old_assoc['theId']
    
    assocParams = ClassAssociationParameters(
      envName=assoc.theEnvironmentName,
      headName=assoc.theHeadAsset,
      headDim='asset',
      headNav=assoc.theHeadNav,
      headType=assoc.theHeadType,
      headMultiplicity=assoc.theHeadMultiplicity,
      headRole=assoc.theHeadRole,
      tailRole=assoc.theTailRole,
      tailMultiplicity=assoc.theTailMultiplicity,
      tailType=assoc.theTailType,
      tailNav=assoc.theTailNav,
      tailDim='asset',
      tailName=assoc.theTailAsset,
      rationale=asset.theRationale)
    assocParams.setId(id)
    try:
      self.db_proxy.updateClassAssociation(assocParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
