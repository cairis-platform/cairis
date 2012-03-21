#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetParameters.py $ $Id: AssetParameters.py 330 2010-10-31 15:01:28Z shaf $
import ObjectCreationParameters

class AssetParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,assetName,shortCode,assetDesc,assetSig,assetType,cFlag,cRationale,cProperties):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = assetName
    self.theShortCode = shortCode
    self.theDescription = assetDesc
    self.theSignificance = assetSig
    self.theEnvironmentProperties = cProperties
    self.theType = assetType
    self.isCritical = cFlag
    self.theCriticalRationale = cRationale

  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def significance(self): return self.theSignificance
  def type(self): return self.theType
  def environmentProperties(self): return self.theEnvironmentProperties
  def critical(self): return self.isCritical
  def criticalRationale(self): return self.theCriticalRationale
