#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TemplateAsset.py $ $Id: TemplateAsset.py 424 2011-02-25 21:29:47Z shaf $

class TemplateAsset:
  def __init__(self,assetId,assetName,shortCode,assetDescription,assetSig,assetType,cFlag,cRationale,cProperty,iProperty,avProperty,acProperty,anProperty,panProperty,unlProperty,unoProperty,cRat = '',iRat = '',avRat = '',acRat = '',anRat = '',panRat = '',unlRat = '',unoRat = ''):
    self.theId = assetId
    self.theName = assetName
    self.theShortCode = shortCode
    self.theDescription = assetDescription
    self.theSignificance = assetSig
    self.theType = assetType
    self.isCritical = cFlag
    self.theCriticalRationale = cRationale
    self.theConfidentialityProperty = cProperty
    self.theIntegrityProperty = iProperty
    self.theAvailabilityProperty = avProperty
    self.theAccountabilityProperty = acProperty
    self.theAnonymityProperty = anProperty
    self.thePseudonymityProperty = panProperty
    self.theUnlinkabilityProperty = unlProperty
    self.theUnobservabilityProperty = unoProperty
    self.theConfidentialityRationale = cRat
    self.theIntegrityRationale = iRat
    self.theAvailabilityRationale = avRat
    self.theAccountabilityRationale = acRat
    self.theAnonymityRationale = anRat
    self.thePseudonymityRationale = panRat
    self.theUnlinkabilityRationale = unlRat
    self.theUnobservabilityRationale = unoRat


    self.valueLookup = {}
    self.valueLookup['None'] = 0
    self.valueLookup['Low'] = 1
    self.valueLookup['Medium'] = 2
    self.valueLookup['High'] = 3

  def id(self): return self.theId
  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def significance(self): return self.theSignificance
  def type(self): return self.theType
  def critical(self): return self.isCritical
  def criticalRationale(self): return self.theCriticalRationale
  def confidentialityProperty(self): return self.theConfidentialityProperty
  def integrityProperty(self): return self.theIntegrityProperty
  def availabilityProperty(self): return self.theAvailabilityProperty
  def accountabilityProperty(self): return self.theAccountabilityProperty
  def anonymityProperty(self): return self.theAnonymityProperty
  def pseudonymityProperty(self): return self.thePseudonymityProperty
  def unlinkabilityProperty(self): return self.theUnlinkabilityProperty
  def unobservabilityProperty(self): return self.theUnobservabilityProperty

  def securityProperties(self):
    cValue = self.valueLookup[self.theConfidentialityProperty]
    iValue = self.valueLookup[self.theIntegrityProperty]
    avValue = self.valueLookup[self.theAvailabilityProperty]
    acValue = self.valueLookup[self.theAccountabilityProperty]
    anValue = self.valueLookup[self.theAnonymityProperty]
    panValue = self.valueLookup[self.thePseudonymityProperty]
    unlValue = self.valueLookup[self.theUnlinkabilityProperty]
    unoValue = self.valueLookup[self.theUnobservabilityProperty]
    return [cValue,iValue,avValue,acValue,anValue,panValue,unlValue,unoValue]

  def rationale(self):
    return [self.theConfidentialityRationale,self.theIntegrityRationale,self.theAvailabilityRationale,self.theAccountabilityRationale,self.theAnonymityRationale,self.thePseudonymityRationale,self.theUnlinkabilityRationale,self.theUnobservabilityRationale]
