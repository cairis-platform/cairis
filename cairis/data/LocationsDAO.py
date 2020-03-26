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
from cairis.core.Location import Location
from cairis.core.Locations import Locations
from cairis.core.LocationsParameters import LocationsParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import LocationModel,LocationsModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.misc.LocationModel import LocationModel as GraphicalLocationModel
__author__ = 'Shamal Faily'


class LocationsDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'locations')

  def get_objects(self,constraint_id = -1):
    try:
      locs = self.db_proxy.getLocations(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    locsKeys = sorted(locs.keys())
    locsList = []
    for key in locsKeys:
      locsList.append(self.simplify(locs[key]))
    return locsList

  def get_object_by_name(self, locations_name):
    locsList = self.get_objects()
    if locsList is None or len(locsList) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Locations')
    for locs in locsList:
      if (locs.name() == locations_name):
        return locs
    self.close()
    raise ObjectNotFoundHTTPError('The provided Locations parameters')

  def add_object(self, locs):
    p = LocationsParameters(
      locsName=locs.name(),
      locsDiagram=locs.diagram(),
      locs=locs.locations(),
      links=[])
    try:
      self.db_proxy.addLocations(p)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object(self,locs,name):
    locs_id = self.db_proxy.getDimensionId(name, 'locations')
    p = LocationsParameters(
      locsName=locs.name(),
      locsDiagram=locs.diagram(),
      locs=locs.locations(),
      links=[])
    p.setId(locs_id)
    try:
      self.db_proxy.updateLocations(p)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      locs_id = self.db_proxy.getDimensionId(name, 'locations')
      self.db_proxy.deleteLocations(locs_id)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, LocationsModel.required)
    json_dict['__python_obj__'] = Locations.__module__+'.'+ Locations.__name__

    loc_list = self.convert_loc_list(fake_loc_list=json_dict['theLocations'])
    json_dict['theLocations'] = []

    locs = json_serialize(json_dict)
    locs = json_deserialize(locs)
    locs.theLocations = loc_list
    locs.theLinks = []

    if isinstance(locs, Locations):
      return locs 
    else:
      self.close()
      raise MalformedJSONHTTPError()

  def simplify(self, obj):
    assert isinstance(obj, Locations)
    del obj.theId
    del obj.theLinks
    obj.theLocations = self.convert_loc_list(real_loc_list=obj.theLocations)
    return obj

  def convert_loc_list(self,real_loc_list = None, fake_loc_list = None):
    new_loc_list = []
    if real_loc_list is not None:
      if len(real_loc_list) > 0:
        for real_loc in real_loc_list:
          assert isinstance(real_loc,Location)
          loc_dict = {}
          loc_dict['theName'] = real_loc.name()
          loc_dict['theAssetInstances'] = []  
          for ai in real_loc.assetInstances():
            loc_dict['theAssetInstances'].append({'theName':ai[0],'theAsset':ai[1]})  
          loc_dict['thePersonaInstances'] = []  
          for pi in real_loc.personaInstances():
            loc_dict['thePersonaInstances'].append({'theName':pi[0],'thePersona':pi[1]})  
          loc_dict['theLinks'] = real_loc.links()
          new_loc_list.append(loc_dict)
    elif fake_loc_list is not None:
      if len(fake_loc_list) > 0:
        for fake_loc in fake_loc_list:
          check_required_keys(fake_loc,LocationModel.required) 
          assetInstances = []
          for ai in fake_loc['theAssetInstances']:
            assetInstances.append((ai['theName'],ai['theAsset']))
          personaInstances = []
          for pi in fake_loc['thePersonaInstances']:
            personaInstances.append((pi['theName'],pi['thePersona']))
          new_loc_list.append(Location(-1,fake_loc['theName'],assetInstances,personaInstances,fake_loc['theLinks']))
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_loc_list', 'fake_loc_list'])
    return new_loc_list

  def get_locations_model(self, locations_name, environment_name, pathValues = []):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    try:
      riskOverlay = self.db_proxy.locationsRiskModel(locations_name,environment_name) 
      lModel = GraphicalLocationModel(locations_name,environment_name, riskOverlay,db_proxy=self.db_proxy, font_name=fontName, font_size=fontSize)
      dot_code = lModel.graph()
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except Exception as ex:
      print(ex)
