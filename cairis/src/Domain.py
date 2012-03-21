#$URL $Id: Domain.py 249 2010-05-30 17:07:31Z shaf $

class Domain:
  def __init__(self,rmId,modName,shortCode,modDesc,domType,giveInd,domains):
    self.theId = rmId
    self.theModuleName = modName
    self.theShortCode = shortCode
    self.theDescription = modDesc
    self.theType = domType
    self.isGiven = giveInd
    self.theDomains = domains

  def id(self): return self.theId
  def name(self): return self.theModuleName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def type(self): return self.theType
  def given(self): return self.isGiven
  def domains(self): return self.theDomains
