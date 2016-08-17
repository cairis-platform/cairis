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

from collections import OrderedDict
import logging

from flask.ext.restful import fields
from flask.ext.restful_swagger import swagger

__author__ = 'Robin Quetin, Shamal Faily'
obj_id_field = '__python_obj__'
def gen_class_metadata(class_ref):
  return {"enum": [class_ref.__module__+'.'+class_ref.__name__]}


@swagger.model
class Contributor(object):
  resource_fields = {
    obj_id_field: fields.String,
    'firstName': fields.String,
    'surname': fields.String,
    'affliation': fields.String,
    'role': fields.String
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    obj_id_field: {
      'enum': [__name__+'.Contributor']
    }
  }

  def __init__(self, first_name=None, surname=None, affliation=None, role=None, tuple_form=None):
    """
    :type first_name: str
    :type surname: str
    :type affliation: str
    :type role: str
    :type tuple_form: tuple
    """
    if tuple_form is None:
      self.firstName = first_name or ''
      self.surname = surname or ''
      self.affliation = affliation or ''
      self.role = role or ''
    else:
      attrs = ['firstName', 'surname', 'affliation', 'role']
      for idx in range(0, len(tuple_form)):
        self.__setattr__(attrs[idx], tuple_form[idx] or '')


@swagger.model
class EnvironmentTensionModel(object):
  # region Swagger Doc
  resource_fields = {
    obj_id_field: fields.String,
    "base_attr_id": fields.Integer,
    "attr_id": fields.Integer,
    "value": fields.Integer,
    "rationale": fields.String
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    obj_id_field: {
      "enum": ["tools.PseudoClasses."+__name__]
    },
    "base_attr_id": {
      "enum": range(0,4)
    },
    "attr_id": {
      "enum": range(4,8)
    },
    "value": {
      "enum": [-1,0,1]
    }
  }
  attr_dictionary = {
    'Confidentiality': 0,
    'Integrity': 1,
    'Availability': 2,
    'Accountability': 3,
    'Anonymity': 4,
    'Pseudonymity': 5,
    'Unlinkability': 6,
    'Unobservability': 7
  }
  attr_dictionary = OrderedDict(sorted(attr_dictionary.items(), key=lambda t: t[1]))
  # endregion

  base_attr_values = range(-1,4)
  attr_values = range(4,8)
  attr_values.append(-1)

  def __init__(self, base_attr_id=-1, attr_id=-1, value=0, rationale='None', key=None):
    """
    :type base_attr_id: int
    :type attr_id: int
    :type value: int|tuple
    :type rationale: str
    :type key: tuple
    """
    if key is not None:
      base_attr_id = key[0]
      attr_id = key[1]
      rationale = value[1]
      value = value[0]

    if base_attr_id not in self.base_attr_values or attr_id not in self.attr_values:
      raise ValueError('Base attribute or subattribute value is incorrect.')

    self.base_attr_id = base_attr_id
    self.attr_id = attr_id
    self.value = value
    self.rationale = rationale


@swagger.model
class Revision(object):
  # region Swagger Docs
  resource_fields = {
    obj_id_field: fields.String,
    'id': fields.Integer,
    'date': fields.String,
    'description': fields.String
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    obj_id_field: { 'enum': [ __name__ + '.Revision'] },
    'date' : { 'enum': ['YY-MM-DD hh:mm:ss'] }
  }
  # endregion

  def __init__(self, id=None, date=None, description=None, tuple_form=None):
    """
    :type id: int
    :type date: str
    :type description: str
    :type tuple_form: tuple
    """
    if tuple_form is None:
      self.id = id
      self.date = date
      self.description = description
    else:
      attrs = ['id', 'date', 'description']
      for idx in range(0, len(tuple_form)):
        self.__setattr__(attrs[idx], tuple_form[idx] or '')


@swagger.model
@swagger.nested(
  contributions=Contributor.__name__,
  revisions=Revision.__name__
)
class ProjectSettings(object):
  # region Swagger Docs
  resource_fields = {
    obj_id_field: fields.String,
    'fontName': fields.String,
    'apFontSize': fields.String,
    'projectName': fields.String,
    'richPicture': fields.String,
    'fontSize': fields.String,
    'projectScope': fields.String,
    'definitions': fields.String,
    'projectGoals': fields.String,
    'contributions': fields.List(fields.Nested(Contributor.resource_fields)),
    'projectBackground': fields.String,
    'revisions': fields.List(fields.Nested(Revision.resource_fields))
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    obj_id_field: {
     'enum': [__name__+'.ProjectSettings']
    }
  }
  # endregion
  req_p_settings_keys = ['AP Font Size', 'Font Name', 'Font Size', 'Project Background', 'Project Goals', 'Project Name', 'Project Scope', 'Rich Picture']

  def __init__(self, pSettings=None, pDict=None, contributors=None, revisions=None):
    logger = logging.getLogger('cairisd')
    project_settings = pSettings or {}

    self.apFontSize = project_settings.get("AP Font Size", "13")
    self.fontName = project_settings.get("Font Name", "Times New Roman")
    self.fontSize = project_settings.get("Font Size", "7.5")
    self.projectBackground = project_settings.get("Project Background", "")
    self.projectGoals = project_settings.get("Project Goals", "")
    self.projectName = project_settings.get("Project Name", "")
    self.projectScope = project_settings.get("Project Scope", "")
    self.richPicture = project_settings.get("Rich Picture", "")

    self.definitions = pDict or {}
    self.contributions = []
    for contributor in contributors or []:
      if isinstance(contributor, tuple):
        new_contr = Contributor(tuple_form=contributor)
        self.contributions.append(new_contr)
      else:
        logger.warning('Item does not meet typical contributor structure. Passing this one.')

    self.revisions = []
    for revision in revisions or []:
      if isinstance(revision, tuple):
        new_rev = Revision(tuple_form=revision)
        self.revisions.append(new_rev)
      else:
        logger.warning('Item does not meet typical contributor structure. Passing this one.')


@swagger.model
class RiskScore(object):
  # region Swagger Docs
  resource_fields = {
    obj_id_field: fields.String,
    'responseName': fields.String,
    'unmitScore': fields.Integer,
    'mitScore': fields.Integer,
    'details': fields.String
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    obj_id_field: { 'enum': [__name__+'.RiskScore'] }
  }
  # endregion
  def __init__(self, response_name, unmit_score, mit_score, details):
    """
    :type response_name: str
    :type unmit_score: int
    :type mit_score: int
    :type details: str
    """
    self.responseName = response_name
    self.unmitScore = unmit_score or -1
    self.mitScore = mit_score or -1
    self.details = details


@swagger.model
class RiskRating(object):
  # region Swagger Doc
  resource_fields = {
    obj_id_field: fields.String,
    'rating': fields.String,
    'threat': fields.String,
    'vulnerability': fields.String,
    'environment': fields.String
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    obj_id_field: { 'enum': [__name__+'.RiskRating'] }
  }
  # endregion
  def __init__(self, threat, vulnerability, environment, rating=None):
    self.threat = threat
    self.vulnerability = vulnerability
    self.environment = environment
    self.rating = rating

@swagger.model
class CountermeasureTarget(object):
  def __init__(self, tName=None, tEffectiveness=None, tRat=None):
    """
    :type tName: str
    :type tEffectiveness: str
    :type tRat: str
    """
    self.theName = tName
    self.theEffectiveness = tEffectiveness
    self.theRationale = tRat

  # region Swagger Doc
  resource_fields = {
    "__python_obj__": fields.String,
    "theName": fields.String,
    "theEffectiveness": fields.String,
    "theRationale": fields.String
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    "theEffectiveness": {
      "enum": [
        "None",
        "Low",
        "Medium",
        "High"
       ]
    } 
  }
  # endregion
  def name(self): return self.theName
  def effectiveness(self): return self.theEffectiveness
  def rationale(self): return self.theRationale


@swagger.model
class PersonaTaskCharacteristics(object):
  def __init__(self, pName, pDur, pFreq, pDemands, pGoalConflict):
    """
    :type pName: str
    :type pDur: str
    :type pFreq: str
    :type pDemands: str
    :type pGoalConflict: str
    """
    self.thePersona = pName
    self.theDuration = pDur
    self.theFrequency = pFreq
    self.theDemands = pDemands
    self.theGoalConflict = pGoalConflict

  # region Swagger Doc
  resource_fields = {
    "__python_obj__": fields.String,
    "thePersona": fields.String,
    "theDuration": fields.String,
    "theFrequency": fields.String,
    "theDemands": fields.String,
    "theGoalConflict": fields.String
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    "theDuration": {
      "enum": [
        "Low",
        "Medium",
        "High"
       ]
    },
    "theFrequency": {
      "enum": [
        "Low",
        "Medium",
        "High"
       ]
    },
    "theDemands": {
      "enum": [
        "None",
        "Low",
        "Medium",
        "High"
       ]
    },
    "theGoalConflict": {
      "enum": [
        "None",
        "Low",
        "Medium",
        "High"
       ]
    }
  }
  # endregion
  def persona(self): return self.thePersona
  def duration(self): return self.theDuration
  def frequency(self): return self.theFrequency
  def demands(self): return self.theDemands
  def goalConflict(self): return self.theGoalConflict




@swagger.model
class SecurityAttribute(object):
  def __init__(self, name=None, value=None, rationale=None):
    """
    :type name: str
    :type value: str
    :type rationale: str
    """
    self.name = name
    self.value = value
    self.rationale = rationale

  # region Swagger Doc
  resource_fields = {
    "__python_obj__": fields.String,
    "name": fields.String,
    "value": fields.String,
    "rationale": fields.String
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    "__python_obj__": {
      "enum": ["tools.PseudoClasses.SecurityAttribute"]
    },
    "name": {
      "enum": [
        'Confidentiality',
        'Integrity',
        'Availability',
        'Accountability',
        'Anonymity',
        'Pseudonymity',
        'Unlinkability',
        'Unobservability'
      ]
    },
    "value": {
      "enum": [
        "None",
        "Low",
        "Medium",
        "High"
       ]
    } 
  }
  # endregion

  def get_attr_value(self, enum_obj):
    """
    Gets the database value for the security attribute
    :type enum_obj: list|tuple
    """
    value = 0

    if self.value is not None:
      found = False
      idx = 0

      while not found and idx < len(enum_obj):
        if enum_obj[idx] == self.value:
          value = idx
          found = True
        else:
          idx += 1

    return value


@swagger.model
class ValuedRole(object):
  # region Swagger Doc
  resource_fields = {
    obj_id_field: fields.String,
    'roleName': fields.String,
    'cost': fields.String
  }
  required = resource_fields.keys()
  required.remove(obj_id_field)
  swagger_metadata = {
    obj_id_field: { 'enum': [__name__+'.ValuedRole'] }
  }
  # endregion
  def __init__(self, role_name, cost):
    self.roleName = role_name
    self.cost = cost
