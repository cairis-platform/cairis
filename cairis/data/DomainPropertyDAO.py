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
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.DomainProperty import DomainProperty
from cairis.core.DomainPropertyParameters import DomainPropertyParameters
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.misc.KaosModel import KaosModel
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import DomainPropertyModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
__author__ = 'Shamal Faily'


class DomainPropertyDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'domainproperty')

  def get_objects(self, constraint_id=-1):
    try:
      domain_properties = self.db_proxy.getDomainProperties(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    dpKeys = sorted(domain_properties.keys())
    dpList = []
    for key in dpKeys:
      value = domain_properties[key]
      dpList.append(self.simplify(value))
    return dpList

  def get_object_by_name(self, name, simplify=True):
    try:
      dpId = self.db_proxy.getDimensionId(name,'domainproperty')
      domain_properties = self.db_proxy.getDomainProperties(dpId)
      found_domain_property = domain_properties.get(name, None)
      if found_domain_property is None:
        self.close()
        raise ObjectNotFoundHTTPError('The provided domain property name')
      return self.simplify(found_domain_property)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided domain property name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def add_object(self, domain_property):
    domain_property_params = DomainPropertyParameters(
      name=domain_property.name(),
      desc=domain_property.description(),
      dpType=domain_property.type(),
      dpOrig=domain_property.originator(),
      tags=domain_property.tags()
    )

    try:
      if not self.check_existing_domain_property(domain_property.name()):
        self.db_proxy.addDomainProperty(domain_property_params)
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=domain_property.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, domain_property, name):

    domain_property_params = DomainPropertyParameters(
      name=domain_property.name(),
      desc=domain_property.description(),
      dpType=domain_property.type(),
      dpOrig=domain_property.originator(),
      tags=domain_property.tags()
    )

    try:
      dpId = self.db_proxy.getDimensionId(name,'domainproperty')
      domain_property_params.setId(dpId)
      self.db_proxy.updateDomainProperty(domain_property_params)
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
      dpId = self.db_proxy.getDimensionId(name,'domainproperty')
      self.db_proxy.deleteDomainProperty(dpId)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError(ex)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_domain_property(self, name):
    try:
      self.db_proxy.nameCheck(name, 'domainproperty')
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


  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, DomainPropertyModel.required)
    json_dict['__python_obj__'] = DomainProperty.__module__ + '.' + DomainProperty.__name__

    domain_property = json_serialize(json_dict)
    domain_property = json_deserialize(domain_property)
    if not isinstance(domain_property, DomainProperty):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return domain_property

  def simplify(self, obj):
    assert isinstance(obj, DomainProperty)
    del obj.theId
    return obj
