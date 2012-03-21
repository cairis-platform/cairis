#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Threat.py $ $Id: Threat.py 429 2011-02-27 17:34:37Z shaf $
from PropertyHolder import PropertyHolder
from numpy import *

class Threat:
  def __init__(self,threatId,threatName,threatType,threatMethod,cProps):
    self.theId = threatId
    self.theThreatName = threatName
    self.theType = threatType
    self.theMethod = threatMethod
    self.theEnvironmentProperties = cProps
    self.theEnvironmentDictionary = {}
    self.theThreatPropertyDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p
      self.theThreatPropertyDictionary[environmentName] = PropertyHolder(p.properties())
    self.likelihoodLookup = {}
    self.likelihoodLookup['Incredible'] = 0
    self.likelihoodLookup['Improbable'] = 1
    self.likelihoodLookup['Remote'] = 2
    self.likelihoodLookup['Occasional'] = 3
    self.likelihoodLookup['Probable'] = 4
    self.likelihoodLookup['Frequent'] = 5

  def id(self): return self.theId
  def name(self): return self.theThreatName
  def type(self): return self.theType
  def method(self): return self.theMethod
  def environmentProperties(self): return self.theEnvironmentProperties

  def likelihood(self,environmentName,dupProperty='',overridingEnvironment=''): 
    if ((dupProperty == '') or (dupProperty == 'None')):
      return (self.theEnvironmentDictionary[environmentName]).likelihood()
    else:
      workingLikelihood = 'Incredible'
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        currentLikelihood = p.likelihood()
        if (dupProperty == 'Override'):
          if (environmentName != overridingEnvironment):
            continue
          else:
            workingLikelihood = currentLikelihood
        else:
          if (self.likelihoodLookup[currentLikelihood] > self.likelihoodLookup[workingLikelihood]):
            workingLikelihood = currentLikelihood
      return workingLikelihood

  def assets(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).assets()
    else:
      mergedAssets = []
      for p in self.theEnvironmentProperties:
        mergedAssets += p.assets()
      return set(mergedAssets)


  def attackers(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).attackers()
    else:
      mergedAttackers = []
      for p in self.theEnvironmentProperties:
        mergedAttackers += p.attackers()
      return set(mergedAttackers)

  def propertyList(self,environmentName,dupProperty,overridingEnvironment):
    if (dupProperty == ''):
      return (self.theThreatPropertyDictionary[environmentName]).propertyList()
    else:
      workingProperties = array((0,0,0,0,0,0,0,0))
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        currentEnvironmentProperties = p.properties()
        for idx,value in enumerate(currentEnvironmentProperties):
          if (workingProperties[idx] == 0 and value != 0):
            workingProperties[idx] = value
          elif (value != 0):
            if (dupProperty == 'Override'):
              if (environmentName != overridingEnvironment):
                continue
              else:
                workingProperties[idx] = value
            else:
              if (value > workingProperties[idx]):
                workingProperties[idx] = value
      return PropertyHolder(workingProperties).propertyList()

  def securityProperties(self,environmentName,dupProperty='',overridingEnvironment=''):
    try:
      return (self.theThreatPropertyDictionary[environmentName]).properties()
    except KeyError:
      workingProperties = array((0,0,0,0,0,0,0,0))
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        currentEnvironmentProperties = p.properties()
        for idx,value in enumerate(currentEnvironmentProperties):
          if (workingProperties[idx] == 0 and value != 0):
            workingProperties[idx] = value
          elif (value != 0):
            if (dupProperty == 'Override'):
              if (environmentName != overridingEnvironment):
                continue
              else:
                workingProperties[idx] = value
            else:
              if (value > workingProperties[idx]):
                workingProperties[idx] = value
      return workingProperties

