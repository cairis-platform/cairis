#$URL $Id: DomainParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class DomainParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,modName,shortCode,modDesc,domType,giveInd,domains):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theModuleName = modName
    self.theShortCode = shortCode
    self.theDescription = modDesc
    self.theType = domType
    self.isGiven = giveInd
    self.theDomains = domains

  def name(self): return self.theModuleName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def type(self): return self.theType
  def given(self): return self.isGiven
  def domains(self): return self.theDomains
