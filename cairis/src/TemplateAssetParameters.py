#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TemplateAssetParameters.py $ $Id: TemplateAssetParameters.py 424 2011-02-25 21:29:47Z shaf $
import ObjectCreationParameters

class TemplateAssetParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,assetName,shortCode,assetDesc,assetSig,assetType,cFlag,cRationale,cProperty,iProperty,avProperty,acProperty,anProperty,panProperty,unlProperty,unoProperty):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = assetName
    self.theShortCode = shortCode
    self.theDescription = assetDesc
    self.theSignificance = assetSig
    self.theConfidentialityProperty = cProperty
    self.theIntegrityProperty = iProperty
    self.theAvailabilityProperty = avProperty
    self.theAccountabilityProperty = acProperty
    self.theAnonymityProperty = anProperty
    self.thePseudonymityProperty = panProperty
    self.theUnlinkabilityProperty = unlProperty
    self.theUnobservabilityProperty = unoProperty
    self.theType = assetType
    self.isCritical = cFlag
    self.theCriticalRationale = cRationale

  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def significance(self): return self.theSignificance
  def type(self): return self.theType
  def confidentialityProperty(self): return self.theConfidentialityProperty
  def integrityProperty(self): return self.theIntegrityProperty
  def availabilityProperty(self): return self.theAvailabilityProperty
  def accountabilityProperty(self): return self.theAccountabilityProperty
  def anonymityProperty(self): return self.theAnonymityProperty
  def pseudonymityProperty(self): return self.thePseudonymityProperty
  def unlinkabilityProperty(self): return self.theUnlinkabilityProperty
  def unobservabilityProperty(self): return self.theUnobservabilityProperty
  def critical(self): return self.isCritical
  def criticalRationale(self): return self.theCriticalRationale
