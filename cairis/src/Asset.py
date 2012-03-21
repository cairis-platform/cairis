#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Asset.py $ $Id: Asset.py 429 2011-02-27 17:34:37Z shaf $
from PropertyHolder import PropertyHolder;
from numpy import *

class Asset:
  def __init__(self,assetId,assetName,shortCode,assetDescription,assetSig,assetType,cFlag,cRationale,cProps):
    self.theId = assetId
    self.theName = assetName
    self.theShortCode = shortCode
    self.theDescription = assetDescription
    self.theSignificance = assetSig
    self.theType = assetType
    self.isCritical = cFlag
    self.theCriticalRationale = cRationale
    self.theEnvironmentProperties = cProps
    self.theEnvironmentDictionary = {}
    self.theAssetPropertyDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p
      self.theAssetPropertyDictionary[environmentName] = PropertyHolder(p.properties())

  def securityProperties(self,environmentName,dupProperty='',overridingEnvironment=''):
    try:
      return (self.theAssetPropertyDictionary[environmentName]).properties()
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
      

  def id(self): return self.theId
  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def significance(self): return self.theSignificance
  def type(self): return self.theType
  def critical(self): return self.isCritical
  def criticalRationale(self): return self.theCriticalRationale
  def environmentProperties(self): return self.theEnvironmentProperties
  def propertyList(self,environmentName,dupProperty,overridingEnvironment): 
    if (len(dupProperty) == 0):
      return (self.theAssetPropertyDictionary[environmentName]).propertyList()
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
