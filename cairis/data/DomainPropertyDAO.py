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
    """
    :raise CairisHTTPError:
    """
    CairisDAO.__init__(self, session_id)

  def get_domain_properties(self, constraint_id=-1, simplify=True):
    """
    :rtype: dict[str,DomainProperty]
    :return
    :raise ARMHTTPError:
    """
    try:
      domain_properties = self.db_proxy.getDomainProperties(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if simplify:
      for key, value in list(domain_properties.items()):
        domain_properties[key] = self.simplify(value)

    return domain_properties

  def get_domain_property_by_name(self, name, simplify=True):
    """
    :rtype: DomainProperty
    :raise ObjectNotFoundHTTPError:
    """
    domain_properties = self.get_domain_properties(simplify=simplify)
    found_domain_property = domain_properties.get(name, None)

    if found_domain_property is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided domain_property name')

    return found_domain_property

  def add_domain_property(self, domain_property):
    """
    :type domain_property: DomainProperty
    :rtype: int
    :raise ARMHTTPError:
    """
    domain_property_params = DomainPropertyParameters(
      name=domain_property.name(),
      desc=domain_property.description(),
      dpType=domain_property.type(),
      dpOrig=domain_property.originator(),
      tags=domain_property.tags()
    )

    try:
      if not self.check_existing_domain_property(domain_property.name()):
        new_id = self.db_proxy.addDomainProperty(domain_property_params)
        return new_id
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=domain_property.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_domain_property(self, domain_property, name):
    found_domain_property = self.get_domain_property_by_name(name, simplify=False)


    domain_property_params = DomainPropertyParameters(
      name=domain_property.name(),
      desc=domain_property.description(),
      dpType=domain_property.type(),
      dpOrig=domain_property.originator(),
      tags=domain_property.tags()
    )
    domain_property_params.setId(found_domain_property.id())

    try:
      self.db_proxy.updateDomainProperty(domain_property_params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_domain_property(self, name):
    found_domain_property = self.get_domain_property_by_name(name, simplify=False)
    domain_property_id = found_domain_property.id()

    try:
      self.db_proxy.deleteDomainProperty(domain_property_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_domain_property(self, name):
    """
    :rtype: bool
    :raise: ARMHTTPError
    """
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
    """
    :rtype : DomainProperty
    :raise MalformedJSONHTTPError:
    """
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
    return obj
