#$URL$ $Id: UseCaseParameters.py 540 2011-11-24 22:08:27Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class UseCaseParameters(ObjectCreationParameters):
  def __init__(self,ucName,ucAuth,ucCode,ucActors,ucDesc,cProps):
    ObjectCreationParameters.__init__(self)
    self.theName = ucName
    self.theAuthor = ucAuth
    self.theCode = ucCode
    self.theActors = ucActors
    self.theDescription = ucDesc
    self.theEnvironmentProperties = cProps


  def name(self): return self.theName
  def author(self): return self.theAuthor
  def code(self): return self.theCode
  def actors(self): return self.theActors
  def description(self): return self.theDescription
  def author(self): return self.theAuthor
  def environmentProperties(self): return self.theEnvironmentProperties
