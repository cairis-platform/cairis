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
from cairis.core.PersonaCharacteristic import PersonaCharacteristic
from cairis.core.ReferenceSynopsis import ReferenceSynopsis
from cairis.core.ReferenceContribution import ReferenceContribution
from cairis.core.PersonaCharacteristicParameters import PersonaCharacteristicParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import PersonaCharacteristicModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.PseudoClasses import CharacteristicReference, CharacteristicReferenceSynopsis, CharacteristicReferenceContribution

__author__ = 'Shamal Faily'


class PersonaCharacteristicDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'persona_characteristic')

  def get_objects(self,constraint_id = -1,simplify=True):
    try:
      pcs = self.db_proxy.getPersonaCharacteristics(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if simplify:
      for key, value in list(pcs.items()):
        del value.theId
        pcs[key] = self.convert_pcrs(real_pc=value) 
        pName,bvName,pcDesc = key.split('/')
        cs = self.db_proxy.getCharacteristicSynopsis(pcDesc)
        crs = CharacteristicReferenceSynopsis(cs.synopsis(),cs.dimension(),cs.actorType(),cs.actor())
        pcs[key].theCharacteristicSynopsis = crs
    return pcs

  def get_objects_summary(self):
    try:
      pcs = self.db_proxy.getPersonaCharacteristicsSummary()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return pcs


  def get_object_by_name(self, persona_characteristic_name):
    pcId = self.db_proxy.getDimensionId(persona_characteristic_name,'persona_characteristic')
    pcs = self.get_objects(pcId)
    if pcs is None or len(pcs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Persona characteristic')
    for key in pcs:
      pName,bvName,pcDesc = key.split('/')
      if (pcDesc == persona_characteristic_name):
        pc = pcs[key]
        return pc
    self.close()
    raise ObjectNotFoundHTTPError('Persona characteristic:\"' + persona_characteristic_name + '\"')

  def add_object(self, pc):
    try:
      self.db_proxy.nameCheck(pc.theName, 'persona_characteristic')
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    pcParams = PersonaCharacteristicParameters(
      pName=pc.thePersonaName,
      modQual=pc.theModQual,
      vName=pc.theVariable,
      cDesc=pc.theName,
      pcGrounds=pc.theGrounds,
      pcWarrant=pc.theWarrant,
      pcBacking=[],
      pcRebuttal=pc.theRebuttal)
    try:
      self.db_proxy.addPersonaCharacteristic(pcParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object(self,pc,name):
    pcParams = PersonaCharacteristicParameters(
      pName=pc.thePersonaName,
      modQual=pc.theModQual,
      vName=pc.theVariable,
      cDesc=pc.theName,
      pcGrounds=pc.theGrounds,
      pcWarrant=pc.theWarrant,
      pcBacking=[],
      pcRebuttal=pc.theRebuttal)
    try:
      pcId = self.db_proxy.getDimensionId(name,'persona_characteristic')
      pcParams.setId(pcId)
      self.db_proxy.updatePersonaCharacteristic(pcParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      pcId = self.db_proxy.getDimensionId(name,'persona_characteristic')
      self.db_proxy.deletePersonaCharacteristic(pcId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, PersonaCharacteristicModel.required)
    json_dict['__python_obj__'] = PersonaCharacteristic.__module__+'.'+ PersonaCharacteristic.__name__
    pc = json_serialize(json_dict)
    pc = json_deserialize(pc)
    pc,ps,rss,rcs = self.convert_pcrs(fake_pc=pc)

    if isinstance(pc, PersonaCharacteristic):
      return pc,ps,rss,rcs
    else:
      self.close()
      raise MalformedJSONHTTPError()

  def convert_pcrs(self,real_pc=None,fake_pc=None):
    if real_pc is not None:
      assert isinstance(real_pc,PersonaCharacteristic)
      pcr_list = []
      if len(real_pc.theGrounds) > 0:
        for real_pcr in real_pc.theGrounds:
          rs = self.db_proxy.getReferenceSynopsis(real_pcr[0])
          crs = CharacteristicReferenceSynopsis(rs.synopsis(),rs.dimension(),rs.actorType(),rs.actor())
          rc = self.db_proxy.getReferenceContribution(real_pc.theName,rs.reference())
          frc = CharacteristicReferenceContribution(rc.meansEnd(),rc.contribution())
          pcr_list.append(CharacteristicReference(real_pcr[0],'grounds',real_pcr[1],real_pcr[2],crs,frc))
        real_pc.theGrounds = pcr_list
      pcr_list = []
      if len(real_pc.theWarrant) > 0:
        for real_pcr in real_pc.theWarrant:
          rs = self.db_proxy.getReferenceSynopsis(real_pcr[0])
          crs = CharacteristicReferenceSynopsis(rs.synopsis(),rs.dimension(),rs.actorType(),rs.actor())
          rc = self.db_proxy.getReferenceContribution(real_pc.theName,rs.reference())
          frc = CharacteristicReferenceContribution(rc.meansEnd(),rc.contribution())
          pcr_list.append(CharacteristicReference(real_pcr[0],'warrant',real_pcr[1],real_pcr[2],crs,frc))
        real_pc.theWarrant = pcr_list
      pcr_list = []
      if len(real_pc.theRebuttal) > 0:
        for real_pcr in real_pc.theRebuttal:
          rs = self.db_proxy.getReferenceSynopsis(real_pcr[0])
          crs = CharacteristicReferenceSynopsis(rs.synopsis(),rs.dimension(),rs.actorType(),rs.actor())
          rc = self.db_proxy.getReferenceContribution(real_pc.theName,rs.reference())
          frc = CharacteristicReferenceContribution(rc.meansEnd(),rc.contribution())
          pcr_list.append(CharacteristicReference(real_pcr[0],'rebuttal',real_pcr[1],real_pcr[2],crs,frc))
        real_pc.theRebuttal = pcr_list
      return real_pc 
    elif fake_pc is not None:
      pcr_list = []
      ps = None
      fcs = fake_pc.theCharacteristicSynopsis
      if (fcs['theSynopsis'] != ""):
        ps = ReferenceSynopsis(-1,fake_pc.theName,fcs['theSynopsis'],fcs['theDimension'],fcs['theActorType'],fcs['theActor'])
      rss = []
      rcs = []
      
      if len(fake_pc.theGrounds) > 0:
        for pcr in fake_pc.theGrounds:
          pcr_list.append((pcr['theReferenceName'],pcr['theReferenceDescription'],pcr['theDimensionName']))
          if (ps != None):
            frs = pcr['theReferenceSynopsis']
            rss.append(ReferenceSynopsis(-1,pcr['theReferenceName'],frs['theSynopsis'],frs['theDimension'],frs['theActorType'],frs['theActor']))
            frc = pcr['theReferenceContribution']
            rcs.append(ReferenceContribution(frs['theSynopsis'],fcs['theSynopsis'],frc['theMeansEnd'],frc['theContribution']))
        fake_pc.theGrounds = pcr_list
      if len(fake_pc.theWarrant) > 0:
        pcr_list = []
        for pcr in fake_pc.theWarrant:
          pcr_list.append((pcr['theReferenceName'],pcr['theReferenceDescription'],pcr['theDimensionName']))
          if (ps != None):
            frs = pcr['theReferenceSynopsis']
            rss.append(ReferenceSynopsis(-1,pcr['theReferenceName'],frs['theSynopsis'],frs['theDimension'],frs['theActorType'],frs['theActor']))
            frc = pcr['theReferenceContribution']
            rcs.append(ReferenceContribution(frs['theSynopsis'],fcs['theSynopsis'],frc['theMeansEnd'],frc['theContribution']))
        fake_pc.theWarrant = pcr_list
      if len(fake_pc.theRebuttal) > 0:
        pcr_list = []
        for pcr in fake_pc.theRebuttal:
          pcr_list.append((pcr['theReferenceName'],pcr['theReferenceDescription'],pcr['theDimensionName']))
          if (ps != None):
            frs = pcr['theReferenceSynopsis']
            rss.append(ReferenceSynopsis(-1,pcr['theReferenceName'],frs['theSynopsis'],frs['theDimension'],frs['theActorType'],frs['theActor']))
            frc = pcr['theReferenceContribution']
            rcs.append(ReferenceContribution(frs['theSynopsis'],fcs['theSynopsis'],frc['theMeansEnd'],frc['theContribution']))
        fake_pc.theRebuttal = pcr_list
      return fake_pc,ps,rss,rcs

  def assignIntentionalElements(self,pcSyn,rSyns,rConts):
    psId = self.db_proxy.synopsisId(pcSyn.synopsis())
    if (psId == -1 and pcSyn.synopsis() != ''):
      self.db_proxy.addCharacteristicSynopsis(pcSyn)
    elif (pcSyn.synopsis() != ''):
      pcSyn.setId(psId)
      self.db_proxy.updateCharacteristicSynopsis(pcSyn)

    for rSyn in rSyns:
      rsId = self.db_proxy.synopsisId(rSyn.synopsis())
      if (rsId == -1 and rSyn.synopsis() != ''):
        self.db_proxy.addReferenceSynopsis(rSyn)
      elif (rSyn.synopsis() != ''):
        rSyn.setId(psId)
        self.db_proxy.updateReferenceSynopsis(rSyn)

    for rCont in rConts:
      if (self.db_proxy.hasContribution('reference',rCont.source(),rCont.destination())):
        self.db_proxy.updateReferenceContribution(rCont)
      elif rCont.meansEnd() != '':
        self.db_proxy.addReferenceContribution(rCont)
