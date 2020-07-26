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


from xml.sax.handler import ContentHandler,EntityResolver
from cairis.core.Borg import Borg
from xml.sax.saxutils import unescape
from cairis.core.ARM import ARMException
import re

__author__ = 'Shamal Faily'

def sanitise(str):
  return re.sub(r'\<[^>]*\>','',str)

def attrsToDict(str):
  g = {}
  for val in list(map(lambda x: x.split('='),str.rstrip(';').split(';'))): g[val[0]] =  val[1]
  return g

class DiagramsNetContentHandler(ContentHandler,EntityResolver):
  def __init__(self,modelType):
    self.theModelType = modelType
    self.theObjects = {}
    self.theAssociations = []
    self.theUpdatedAssociations = []
    self.theTrustBoundaries = {}
    self.theUpdatedTrustBoundaries = {}
    self.theFlows = {}
    self.theUpdatedFlows = []
    self.resetObjectAttributes()
    self.resetTrustBoundaryAttributes()
    self.inFlow = 0

  def resolveEntity(self,publicId,systemId):
    return systemId

  def resetObjectAttributes(self):
    self.theObjectId = 0
    self.inObject = 0 

  def resetTrustBoundaryAttributes(self):
    self.theObjectId = 0
    self.inTrustBoundary = 0 

  def objects(self): return list(self.theObjects.values())
  def flows(self): return self.theUpdatedFlows
  def trustBoundaries(self): return list(self.theUpdatedTrustBoundaries.values())
  def associations(self): return self.theUpdatedAssociations

  def startElement(self,name,attrs):
    if (name == 'object'):
      self.theObjectId = attrs['id']
      if self.theModelType == 'dataflow':
        if 'type' not in attrs:
          if 'assets' not in attrs and self.theObjectId != '0':
            self.theFlows[self.theObjectId] = {'assets' : ['Unknown information']}
          elif 'assets' in attrs and self.theObjectId != '0':
            self.theFlows[self.theObjectId] = {'name' : 'Undefined flow', 'assets' : list(map(lambda v: v.strip(), attrs['assets'].split(','))) }
          self.inFlow = 1
        else:
          objtType = attrs['type'].lower().strip()
          if objtType in ['trust_boundary','trust boundary','trustboundary']:
            if 'name' not in attrs:
              raise ARMException('Trust boundary defined without a name')
            self.theTrustBoundaries[self.theObjectId] = {'name' : sanitise(attrs['name'])}
            self.inTrustBoundary = 1
          else:
            if 'label' not in attrs:
              raise ARMException('DFD object defined without a name')
            objtName = sanitise(attrs['label'])
            if objtType not in ['process','entity','datastore']:
              raise ARMException(objtType + ' is not a valid type for DFD object ' + objtName)
            self.theObjects[self.theObjectId] = {'name' : objtName, 'type' : objtType}
            self.inObject = 1
      elif self.theModelType == 'asset':
        if 'label' not in attrs:
          raise ARMException('Object ' + self.theObjectId + " has no label.")
        assetName = attrs['label'].strip()
        assetType = 'information'
        if 'type' in attrs:
          assetType = attrs['type'].lower().strip()
        if (assetType not in ['hardware','information','people','software','systems']):
          raise ARMException(attrs['type'] + " is an invalid type for asset " + assetName + ".  Valid types are Hardware, Information, People, Software, and Systems.")

        assetSC = 'TBD'
        if 'short_code' in attrs:
          assetSC = attrs['short_code']

        assetDesc = 'To be defined'
        if 'description' in attrs:
          assetDesc = attrs['description']

        assetSig = 'To be defined'
        if 'significance' in attrs:
          assetSig = attrs['significance']

        secProperties = [0,0,0,0,0,0,0,0]
        propRationale = ['None','None','None','None','None','None','None','None']
        secAttrs = ['confidentiality','integrity','availability','accountability','anonymity','pseudonymity','unlinkability','unobservability']
        valueLookup = {'none' : 0, 'low' : 1, 'medium' : 2, 'high' : 3}
        for idx,secAttr in enumerate(secAttrs):
          saKey = ''
          if secAttr in attrs:
            saKey = secAttr
          elif secAttr not in attrs and secAttr.capitalize() in attrs:
            saKey = secAttr.capitalize()

          if saKey != '':
            secProp = attrs[saKey].lower().strip()
            if secProp not in valueLookup:
              raise ARMException(secProp + ' is an invalid ' + secAttr + ' value for asset ' + assetName)
            else:
              propValue = valueLookup[secProp]
              secProperties[idx] = propValue
                 
              prKey = secAttr + '_rationale'
              if prKey in attrs:
                propRationale[idx] = attrs[prKey]
              else:
                if propValue == 0:
                  propRationale[idx] = 'None'
                else:
                  propRationale[idx] = 'To be defined'
          else:
            secProperties[idx] = 0
            propRationale[idx] = 'None' 
        if (secProperties == [0,0,0,0,0,0,0,0]):
          secAttrs = [0,0,1,0,0,0,0,0]
        propRationale = []
        for secProp in secProperties:
          if (secProp == 0):
            propRationale.append('None')
          else:   
            propRationale.append('To be defined')
        self.theObjects[self.theObjectId] = {'name' : assetName, 'short_code' : assetSC, 'type' : assetType.capitalize(), 'description' : assetDesc, 'significance' : assetSig,  'properties' : secProperties, 'rationale' : propRationale} 
    elif (name == 'mxCell' and self.theModelType == 'dataflow' and self.inFlow):
      objectId = self.theObjectId
      if('source' in attrs and 'target' in attrs and self.inFlow):
        if objectId in self.theFlows:
          self.theFlows[objectId]['from_name'] = attrs['source']
          self.theFlows[objectId]['from_type'] = ''
          self.theFlows[objectId]['to_name'] =  attrs['target']
          self.theFlows[objectId]['to_type'] = ''
      elif('parent' in attrs and objectId in self.theFlows and attrs['parent'] != '0'):
        self.theFlows[objectId]['name'] = attrs['value']
        self.inFlow = 0
    elif (name == 'mxCell' and self.theModelType == 'asset' and 'source' in attrs and 'target' in attrs):
      if ('style' not in attrs):
        raise ARMException('Missing style attribute in mxCell id ' + attrs['id'])
      d = attrsToDict(attrs['style'])
      
      headNav = 0
      tailNav = 0
      headType = 'Association'
      tailType = 'Association'

      if (('startArrow' not in d) and ('endArrow' not in d) and ('edgeStyle' in d) and (d['edgeStyle'] == 'orthogonalEdgeStyle')):
        tailNav = 1
      else:
        if (('startArrow' not in d) or (d['startArrow'] == 'None')):
          headType = 'Association'
        elif d['startArrow'] in ['classic','open','openThin']:
          headType = 'Association'
          headNav = 1  
        elif d['startArrow'] in ['diamond','diamondThin']:
          headType = 'Aggregation'
          if d['startFill'] == 1:
            headType = 'Composition'
        elif d['startArrow'] == 'block':
          headType = 'Inheritance'

        if (('endArrow' not in d) or (d['endArrow'] == 'None')):
          tailType = 'Association'
        elif d['endArrow'] in ['classic','open','openThin']:
          tailType = 'Association'
          tailNav = 1  
        elif d['endArrow'] in ['diamond','diamondThin']:
          tailType = 'Aggregation'
          if d['endFill'] == 1:
            tailType = 'Composition'
        elif d['endArrow'] == 'block':
          tailType = 'Inheritance'
     
      self.theAssociations.append({'head' : attrs['source'], 'tail' : attrs['target'], 'headType' : headType, 'headNav' : headNav, 'tailType' : tailType, 'tailNav' : tailNav})

    elif (name == 'mxGeometry' and self.theModelType == 'dataflow'):
      if (self.inObject):
        self.theObjects[self.theObjectId]['minX'] = float(attrs['x'])
        self.theObjects[self.theObjectId]['maxX'] = float(attrs['x']) + float(attrs['width'])
        self.theObjects[self.theObjectId]['minY'] = float(attrs['y'])
        self.theObjects[self.theObjectId]['maxY'] = float(attrs['y']) + float(attrs['height'])
      elif (self.inTrustBoundary):
        self.theTrustBoundaries[self.theObjectId]['minX'] = float(attrs['x'])
        self.theTrustBoundaries[self.theObjectId]['maxX'] = float(attrs['x']) + float(attrs['width'])
        self.theTrustBoundaries[self.theObjectId]['minY'] = float(attrs['y'])
        self.theTrustBoundaries[self.theObjectId]['maxY'] = float(attrs['y']) + float(attrs['height'])


  def endElement(self,name):
    if (name == 'object'):
      if (self.inObject):
        self.resetObjectAttributes() 
      elif (self.inTrustBoundary):
        self.resetTrustBoundaryAttributes() 
    elif (name == 'diagram'):
      if (self.theModelType == 'dataflow'):
        self.updateFlows()
        self.updateTrustBoundaries() 
      elif (self.theModelType == 'asset'):
        self.updateAssociations()
        
  def updateFlows(self):
    validFlowTypes = set([('entity','process'),('process','entity'),('datastore','process'),('process','datastore'),('process','process')])
    for objtKey in self.theFlows:
      f = self.theFlows[objtKey]
      dfName = f['name']
      fromName = self.theObjects[f['from_name']]['name']
      fromType = self.theObjects[f['from_name']]['type']
      toName = self.theObjects[f['to_name']]['name']
      toType = self.theObjects[f['to_name']]['type']
      if ((fromType,toType) not in validFlowTypes):
        raise ARMException('Data flow ' + dfName + ' is invalid because ' + fromType + ' to ' + toType + ' flows are not permissible.')
      else:
        self.theUpdatedFlows.append({'name' : dfName, 'from_name' : fromName, 'from_type' : fromType, 'to_name' : toName, 'to_type' : toType, 'assets' : f['assets']})

  def updateTrustBoundaries(self):
    for tbKey in self.theTrustBoundaries:
      tbMinX = self.theTrustBoundaries[tbKey]['minX']
      tbMaxX = self.theTrustBoundaries[tbKey]['maxX']
      tbMinY = self.theTrustBoundaries[tbKey]['minY']
      tbMaxY = self.theTrustBoundaries[tbKey]['maxY']
      tbName = self.theTrustBoundaries[tbKey]['name']
      for objtKey in self.theObjects:
        objtName = self.theObjects[objtKey]['name']
        minX = self.theObjects[objtKey]['minX']
        maxX = self.theObjects[objtKey]['maxX']
        minY = self.theObjects[objtKey]['minY']
        maxY = self.theObjects[objtKey]['maxY']
        if (tbMinX <= minX and tbMaxX >= maxX and tbMinY <= minY and tbMaxY >= maxY):
          if (tbKey not in self.theUpdatedTrustBoundaries):
            self.theUpdatedTrustBoundaries[tbKey] = {'name' : tbName, 'components' : []}
          compType = self.theObjects[objtKey]['type']
          if (compType == 'entity'):
            raise ARMException("Cannot add entity " + objtName + " to trust boundary " + tbName + ". Entities are invalid trust boundary components.")
          else:
            self.theUpdatedTrustBoundaries[tbKey]['components'].append({'name' : objtName, 'type' : compType})

  def updateAssociations(self):
    for assoc in self.theAssociations:
      self.theUpdatedAssociations.append({'head' : self.theObjects[assoc['head']]['name'], 'headType' : assoc['headType'], 'headNav' : assoc['headNav'], 'tail' : self.theObjects[assoc['tail']]['name'], 'tailType' : assoc['tailType'], 'tailNav' : assoc['tailNav']})
