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

from flask_restful import fields
from cairis.core.ReferenceSynopsis import ReferenceSynopsis
from cairis.core.ReferenceContribution import ReferenceContribution

__author__ = 'Robin Quetin, Shamal Faily'
obj_id_field = '__python_obj__'
def gen_class_metadata(class_ref):
  return {"enum": [class_ref.__module__+'.'+class_ref.__name__]}

class CharacteristicReferenceSynopsis(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theSynopsis": fields.String,
    "theDimension": fields.String,
    "theActorType": fields.String,
    "theActor": fields.String,
    "theInitialSatisfaction" : fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self, rsName='', rsDim='', rsActorType='', rsActor='', gSat=''):
    self.theSynopsis = rsName
    self.theDimension = rsDim
    self.theActorType = rsActorType
    self.theActor= rsActor
    self.theInitialSatisfaction = gSat

  def __getitem__(self,varName):
    if (varName == 'theSynopsis'): return self.theSynopsis
    elif (varName == 'theDimension'): return self.theDimension
    elif (varName == 'theActorType'): return self.theActorType
    elif (varName == 'theActor'): return self.theActor
    elif (varName == 'theInitialSatisfaction'): return self.theInitialSatisfaction
    else: return None

class CharacteristicReferenceContribution(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theMeansEnd": fields.String,
    "theContribution": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self, rcMe='', rcCont=''):
    self.theMeansEnd = rcMe
    self.theContribution = rcCont

  def __getitem__(self,varName):
    if (varName == 'theMeansEnd'): return self.theMeansEnd
    elif (varName == 'theContribution'): return self.theContribution
    else: return None

class CharacteristicReference(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theReferenceName' : fields.String,
    'theCharacteristicType' : fields.String,
    'theReferenceDescription' : fields.String,
    'theDimensionName' : fields.String,
    'theReferenceSynopsis' : fields.Nested(CharacteristicReferenceSynopsis.resource_fields),
    'theReferenceContribution' : fields.Nested(CharacteristicReferenceContribution.resource_fields)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self, refName=None, crTypeName='grounds', refDesc=None, dimName='document',rSyn=None,rCont=None):
    """
    :type refName: str
    :type crTypeName: str
    :type refDesc: str
    :type dimName: str
    """
    self.theReferenceName = refName
    self.theCharacteristicType = crTypeName
    self.theReferenceDescription = refDesc
    self.theDimensionName = dimName
    self.theReferenceSynopsis = rSyn
    self.theReferenceContribution = rCont

class Definition(object):
  resource_fields = {
    obj_id_field: fields.String,
    'name': fields.String,
    'value': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class Contributor(object):
  resource_fields = {
    obj_id_field: fields.String,
    'firstName': fields.String,
    'surname': fields.String,
    'affiliation': fields.String,
    'role': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self, first_name=None, surname=None, affiliation=None, role=None, tuple_form=None):
    """
    :type first_name: str
    :type surname: str
    :type affiliation: str
    :type role: str
    :type tuple_form: tuple
    """
    if tuple_form is None:
      self.firstName = first_name or ''
      self.surname = surname or ''
      self.affiliation = affiliation or ''
      self.role = role or ''
    else:
      attrs = ['firstName', 'surname', 'affiliation', 'role']
      for idx in range(0, len(tuple_form)):
        self.__setattr__(attrs[idx], tuple_form[idx] or '')


class EnvironmentTensionModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "base_attr_id": fields.Integer,
    "attr_id": fields.Integer,
    "value": fields.Integer,
    "rationale": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)
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
  attr_dictionary = OrderedDict(sorted(list(attr_dictionary.items()), key=lambda t: t[1]))
  # endregion

  base_attr_values = list(range(-1,4))
  attr_values = list(range(4,8))
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


class Revision(object):
  resource_fields = {
    obj_id_field: fields.String,
    'id': fields.Integer,
    'date': fields.String,
    'description': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

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

class ProjectSettings(object):
  resource_fields = {
    obj_id_field: fields.String,
    'projectName': fields.String,
    'richPicture': fields.String,
    'projectScope': fields.String,
    'definitions': fields.List(fields.Nested(Definition.resource_fields)),
    'projectGoals': fields.String,
    'contributions': fields.List(fields.Nested(Contributor.resource_fields)),
    'projectBackground': fields.String,
    'revisions': fields.List(fields.Nested(Revision.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)
  req_p_settings_keys = ['Project Background', 'Project Goals', 'Project Name', 'Project Scope', 'Rich Picture']

  def __init__(self, pSettings=None, pDict=None, contributors=None, revisions=None):
    logger = logging.getLogger('cairisd')
    project_settings = pSettings or {}

    self.projectBackground = project_settings.get("Project Background", "")
    self.projectGoals = project_settings.get("Project Goals", "")
    self.projectName = project_settings.get("Project Name", "")
    self.projectScope = project_settings.get("Project Scope", "")
    self.richPicture = project_settings.get("Rich Picture", "")

    self.definitions = pDict or []
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

class RiskScore(object):
  resource_fields = {
    obj_id_field: fields.String,
    'responseName': fields.String,
    'unmitScore': fields.Integer,
    'mitScore': fields.Integer,
    'details': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

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

class RiskRating(object):
  resource_fields = {
    obj_id_field: fields.String,
    'rating': fields.String,
    'threat': fields.String,
    'vulnerability': fields.String,
    'environment': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self, threat, vulnerability, environment, rating=None):
    self.threat = threat
    self.vulnerability = vulnerability
    self.environment = environment
    self.rating = rating

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

  resource_fields = {
    "__python_obj__": fields.String,
    "theName": fields.String,
    "theEffectiveness": fields.String,
    "theRationale": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def name(self): return self.theName
  def effectiveness(self): return self.theEffectiveness
  def rationale(self): return self.theRationale


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

  resource_fields = {
    "__python_obj__": fields.String,
    "thePersona": fields.String,
    "theDuration": fields.String,
    "theFrequency": fields.String,
    "theDemands": fields.String,
    "theGoalConflict": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def persona(self): return self.thePersona
  def duration(self): return self.theDuration
  def frequency(self): return self.theFrequency
  def demands(self): return self.theDemands
  def goalConflict(self): return self.theGoalConflict

class CountermeasureTaskCharacteristics(object):
  def __init__(self, pTask, pName, pDur, pFreq, pDemands, pGoalConflict):
    """
    :type pTask: str
    :type pName: str
    :type pDur: str
    :type pFreq: str
    :type pDemands: str
    :type pGoalConflict: str
    """
    self.theTask = pTask
    self.thePersona = pName
    self.theDuration = pDur
    self.theFrequency = pFreq
    self.theDemands = pDemands
    self.theGoalConflict = pGoalConflict

  resource_fields = {
    "__python_obj__": fields.String,
    "theTask": fields.String,
    "thePersona": fields.String,
    "theDuration": fields.String,
    "theFrequency": fields.String,
    "theDemands": fields.String,
    "theGoalConflict": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def task(self): return self.theTask
  def persona(self): return self.thePersona
  def duration(self): return self.theDuration
  def frequency(self): return self.theFrequency
  def demands(self): return self.theDemands
  def goalConflict(self): return self.theGoalConflict


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

  resource_fields = {
    "__python_obj__": fields.String,
    "name": fields.String,
    "value": fields.String,
    "rationale": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

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


class ValuedRole(object):
  resource_fields = {
    obj_id_field: fields.String,
    'roleName': fields.String,
    'cost': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self, role_name, cost):
    self.roleName = role_name
    self.cost = cost

class ExceptionAttributes(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theName': fields.String,
    'theDimensionType': fields.String,
    'theDimensionValue': fields.String,
    'theCategoryName': fields.String,
    'theDescription': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,excName,dimType,dimValue,catName,excDesc):
    self.theName = excName
    self.theDimensionType = dimType
    self.theDimensionValue = dimValue
    self.theCategoryName = catName
    self.theDescription = excDesc

class StepAttributes(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theStepText': fields.String,
    'theSynopsis': fields.String,
    'theActor': fields.String,
    'theActorType': fields.String,
    'theExceptions': fields.List(fields.Nested(ExceptionAttributes.resource_fields)),
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,stepTxt,stepSyn,stepActor,stepActorType,stepExceptions):
    self.theStepText = stepTxt
    self.theSynopsis = stepSyn
    self.theActor = stepActor
    self.theActorType = stepActorType
    self.theExceptions = stepExceptions

  def synopsis(self): return self.theSynopsis
  def actor(self): return self.theActor
  def actorType(self): return self.theActorType
  def tags(self): return self.theTags
  def setSynopsis(self,s): self.theSynopsis = s
  def setActor(self,a): self.theActor = a

class StepsAttributes(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theSteps': fields.List(fields.Nested(StepAttributes.resource_fields)),
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self):
    self.theSteps = []

  def __getitem__(self,stepNo):
    return self.theSteps[stepNo]

  def __setitem__(self,stepNo,s):
    self.theSteps[stepNo] = s

  def size(self):
    return len(self.theSteps)

  def append(self,s):
    self.theSteps.append(s)

  def remove(self,stepNo):
    self.theSteps.pop(stepNo)

  def insert(self,pos,s):
    self.theSteps.insert(pos,s)

class ObjectDependency(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theDimensionName': fields.String,
    'theObjectName': fields.String,
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,dimension_name,object_name):
    self.theDimensionName = dimension_name
    self.theObjectName = object_name

class TaskGoalContribution(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theSource': fields.String,
    'theDestination': fields.String,
    'theEnvironment': fields.String,
    'theContribution': fields.String,
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,src,dest,env,cont):
    self.theSource = src 
    self.theDestination = dest
    self.theEnvironment = env
    self.theContribution = cont
