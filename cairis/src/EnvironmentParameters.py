#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/EnvironmentParameters.py $ $Id: EnvironmentParameters.py 546 2012-01-16 13:33:20Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class EnvironmentParameters(ObjectCreationParameters):
  def __init__(self,conName,conSc,conDesc,environments = [],duplProperty = 'None',overridingEnvironment = '', envTensions = None):
    ObjectCreationParameters.__init__(self)
    self.theName = conName
    self.theShortCode = conSc
    self.theDescription = conDesc
    self.theEnvironments = environments
    self.theDuplicateProperty = duplProperty 
    self.theOverridingEnvironment = overridingEnvironment
    self.theAssetValues = None
    if (envTensions == None):
      self.theTensions = {}
      defaultTension = (0,'None')
      idx = 0
      while idx < 4:
        iidx = 4
        while iidx < 8:
          self.theTensions[(idx,iidx)] = defaultTension
          iidx += 1
        idx += 1
    else:
      self.theTensions = envTensions

  def setAssetValues(self,avs):
    self.theAssetValues = avs

  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def environments(self): return self.theEnvironments
  def duplicateProperty(self): return self.theDuplicateProperty
  def overridingEnvironment(self): return self.theOverridingEnvironment
  def assetValues(self): return self.theAssetValues
  def tensions(self): return self.theTensions
