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
from cairis.daemon.CairisHTTPError import ARMHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, SilentHTTPError, ObjectNotFoundHTTPError
from cairis.data.CairisDAO import CairisDAO
from cairis.core.Borg import Borg
from cairis.core.dba import createDefaults, dbOwner, dbExists, canonicalDbName
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.PseudoClasses import ProjectSettings, Contributor, Revision, Definition
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin, Shamal Faily'


class ProjectDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'project')

  def clear_project(self, objt = None, pathValues = []):
    try:
      self.db_proxy.clearDatabase(session_id=self.session_id)
      b = Borg()
      ses_settings = b.get_settings(self.session_id)
      dbHost = ses_settings['dbHost']
      dbPort = ses_settings['dbPort']
      dbUser = ses_settings['dbUser']
      dbPasswd = ses_settings['dbPasswd']
      dbName = ses_settings['dbName']
      createDefaults(b.cairisRoot,dbHost,dbPort,dbUser,dbPasswd,dbName)
      return 'Project cleared successfully'
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def create_new_database(self,db_name, pathValues = []):
    try:
      if (db_name in ['null','']):
        raise ARMException('No database name defined')
      if (db_name == 'default'):
        raise ARMException('Cannot create a new default database')

      b = Borg()
      ses_settings = b.get_settings(self.session_id)
      dbUser = ses_settings['dbUser']
      dbName = dbUser + '_' + canonicalDbName(db_name)
      if (dbExists(dbName)):
        raise ARMException(db_name + " already exists")
 
      self.db_proxy.createDatabase(db_name,self.session_id)
      return 'New database successfully created'
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def open_database(self,db_name, pathValues = []):
    try:
      if (db_name in ['null','']):
        raise ARMException('No database name defined')

      dbList = list(map(lambda db: db['database'],self.show_databases()))

      b = Borg()
      ses_settings = b.get_settings(self.session_id)
      dbUser = ses_settings['dbUser']
      currentlyOpenDbName= ses_settings['dbName']
      toOpenDbName = dbUser + '_' + canonicalDbName(db_name)

      if ((db_name not in dbList) and (toOpenDbName != currentlyOpenDbName)):
        raise ObjectNotFound(db_name + " does not exist")
      
      if (db_name == 'default'):
        b = Borg()
        ses_settings = b.get_settings(self.session_id)
        database_owner = ses_settings['dbUser']
      else:
        database_owner = dbOwner(db_name)

      self.db_proxy.openDatabase(database_owner + '_' + db_name,self.session_id)
      return 'Database successfully opened'
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError(db_name + ' does not exist')
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def delete_database(self,db_name, pathValues = []):
    try:
      if (db_name in ['null','']):
        raise ARMException('No database name defined')
      if (db_name not in list(map(lambda db: db['database'],self.show_databases()))):
        raise ObjectNotFound(db_name + " does not exist")
      self.db_proxy.deleteDatabase(db_name,self.session_id)
      return 'Database successfully deleted'
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided asset name')
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def show_databases(self, pathValues = []):
    try:
      b = Borg()
      ses_settings = b.get_settings(self.session_id)
      dbUser = ses_settings['dbUser']
      rows = self.db_proxy.showDatabases(self.session_id)
      dbs = []
      for db,owner in rows:
        permissioned = 'N'
        if (dbUser == owner):
          permissioned = 'Y'
        if (db == 'default'):
          permissioned = 'N'
        dbs.append({"database" : db,"permissioned" : permissioned})
      return dbs
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def get_settings(self,pathValues = []):
    try:
      pSettings = self.db_proxy.getProjectSettings()
      pDict = self.db_proxy.getDictionary()
      contributors = self.db_proxy.getContributors()
      revisions = self.db_proxy.getRevisions()
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

    settings = ProjectSettings(pSettings, pDict, contributors, revisions)
    return settings

  def apply_settings(self, settings, pathValues = []):
    try:
      b = Borg()
      self.db_proxy.updateSettings(
        settings.projectName,
        settings.projectBackground,
        settings.projectGoals,
        settings.projectScope,
        settings.definitions,
        settings.contributions,
        settings.revisions,
        settings.richPicture,
        b.settings[self.session_id]['fontSize'],
        b.settings[self.session_id]['fontName']
      )
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, ProjectSettings.required)
    json_dict['__python_obj__'] = ProjectSettings.__module__+'.'+ProjectSettings.__name__

    contrs = json_dict['contributions'] or []
    if not isinstance(contrs, list):
      contrs = []
    for idx in range(0, len(contrs)):
      try:
        check_required_keys(contrs[idx], Contributor.required)
        json_dict['contributions'][idx] = (contrs[idx]['firstName'], contrs[idx]['surname'], contrs[idx]['affiliation'], contrs[idx]['role'])
      except MissingParameterHTTPError:
        SilentHTTPError('A contribution did not contain all required fields. Skipping this one.')

    revisions = json_dict['revisions'] or []
    if not isinstance(revisions, list):
      revisions = []

    for idx in range(0, len(revisions)):
      try:
        check_required_keys(revisions[idx], Revision.required)
        json_dict['revisions'][idx] = (revisions[idx]['id'], revisions[idx]['date'], revisions[idx]['description'])
      except MissingParameterHTTPError:
        SilentHTTPError('A revision did not contain all required fields. Skipping this one.')

    settings = json_deserialize(json_dict)
    return settings
