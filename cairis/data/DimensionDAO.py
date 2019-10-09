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
from cairis.daemon.CairisHTTPError import CairisHTTPError, ARMHTTPError
from cairis.data.CairisDAO import CairisDAO
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy
from http.client import BAD_REQUEST, NOT_FOUND


__author__ = 'Shamal Faily'


class DimensionDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def getDimensions(self,table,id):
    try:
      permissableDimensions = ['access_right', 'architectural_pattern', 'component_view','asset', 'asset_reference', 'asset_type','attacker','attacker_reference', 'behavioural_variable', 'capability','characteristic_synopsis', 'component', 'concept_reference','connector', 'countermeasure','countermeasure_reference', 'countermeasure_value', 'datastore', 'detection_mechanism', 'dfd_filter', 'document_reference', 'domainproperty','domainproperty_reference', 'entity','environment', 'environment_reference','external_document', 'goal', 'goal_reference','goal_category_type','interface','likelihood','locations','misusability_case','misusecase','misusecase_reference','motivation','obstacle','obstacle_category_type','obstacle_reference','persona','persona_characteristic','persona_characteristic_synopsis','persona_implied_process','persona_reference','persona_type','priority_type', 'privilege', 'process','protocol', 'reference_synopsis','requirement', 'requirement_reference', 'requirement_type','response', 'response_reference', 'risk', 'risk_class','risk_reference','role', 'role_reference', 'role_type', 'securitypattern','severity', 'surface_type', 'task', 'task_characteristic', 'task_reference','template_asset', 'template_goal', 'template_requirement','trace_dimension','threat', 'threat_reference','threat_type', 'threat_value', 'usecase', 'vulnerability','vulnerability_reference', 'vulnerability_type']
      if (table not in permissableDimensions):
        raise CairisHTTPError(BAD_REQUEST,'Invalid dimension',table + ' is not a permissable dimension')
      if (table == 'persona_characteristic_synopsis'):
        return self.getDimensionNames(table,'')
      else: 
        return sorted(self.db_proxy.getDimensions(table,id).keys())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def getDimensionNames(self,table,environment):
    try:
      permissableDimensions = ['asset','asset_value','attacker','countermeasure','datastore','detection_mechanism','domainproperty','dfd_filter','entity','goal','misusecase','obstacle','persona', 'process', 'requirement','response','risk','role','task','task_characteristic', 'threat','usecase', 'vulnerability','component']
      if (table not in permissableDimensions):
        raise CairisHTTPError(BAD_REQUEST,'Invalid dimension',table + ' is not a permissable dimension when specifying environment')
      if (self.db_proxy.nameExists(environment,'environment') == False):
        raise CairisHTTPError(NOT_FOUND,'Unknown environment',environment + ' does not exist')
      return self.db_proxy.getDimensionNames(table,environment)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
