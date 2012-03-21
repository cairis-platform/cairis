#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Mitigation.py $ $Id: Mitigation.py 424 2011-02-25 21:29:47Z shaf $
from AssetParameters import AssetParameters
from numpy import *

class Response:
  def __init__(self,mitId,mitName,mitType,mitDesc,mitCost,mitProperties,detPoint,detMech,mitRisks,mitTargets):
    self.theId = mitId
    self.theName = mitName
    self.theType = mitType
    self.theDescription = mitDesc
    self.theRisks = mitRisks
    self.theCost = mitCost
    self.theMitigatedProperties = mitProperties
    self.theDetectionPoint = detPoint
    self.theDetectionMechanism = detMech
    self.theTargets = mitTargets

  def id(self): return self.theId
  def name(self): return self.theName
  def type(self): return self.theType
  def description(self): return self.theDescription
  def risks(self): return self.theRisks
  def cost(self): return self.theCost
  def properties(self): return self.theMitigatedProperties
  def detectionPoint(self): return self.theDetectionPoint
  def detectionMechanism(self): return self.theDetectionMechanism
  def targets(self): return self.theTargets
  def effectiveness(self):
    if (self.theMitigatedProperties == array((0,0,0,0,0,0,0,0))): return 'None'
    elif (self.theMitigatedProperties == array((1,1,1,1,1,1,1,1))): return 'Low'
    elif (self.theMitigatedProperties == array((2,2,2,2,2,2,2,2))): return 'Medium'
    elif (self.theMitigatedProperties == array((3,3,3,3,3,3,3,3))): return 'High'

  def assetParameters(self,assetId = -1):
    cMitigated = 1
    iMitigated = 1
    avMitigated = 1
    acMitigated = 1
    anMitigated = 1
    panMitigated = 1
    unlMitigated = 1
    unoMitigated = 1
    for idx,propertyName in enumerate(self.theMitigatedProperties):
      if (propertyName == 'Confidentiality'): cMitigated = 3
      elif (propertyName == 'Integrity'): iMitigated = 3
      elif (propertyName == 'Availability'): avMitigated = 3
      elif (propertyName == 'Accountability'): acMitigated = 3
      elif (propertyName == 'Anonymity'): acMitigated = 4
      elif (propertyName == 'Pseudonymity'): acMitigated = 5
      elif (propertyName == 'Unlinkability'): acMitigated = 6
      elif (propertyName == 'Unobservability'): acMitigated = 7
    assetProperties = array((cMitigated,iMitigated,avMitigated,acMitigate,anMitigated,panMitigated,unlMitigated,unoMitigated))
    mitName = self.theName + ' response'
    parameters = AssetParameters(mitName,self.theDescription,assetProperties)
    parameters.setId(assetId)
    return parameters
