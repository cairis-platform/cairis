#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RoleParameters.py $ $Id: RoleParameters.py 395 2011-01-06 01:17:45Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class RoleParameters(ObjectCreationParameters):
  def __init__(self,name,rType,sCode,desc,cProperties):
    ObjectCreationParameters.__init__(self)
    self.theName = name
    self.theShortCode = sCode
    self.theDescription = desc
    self.theType = rType
    self.theEnvironmentProperties = cProperties

  def name(self): return self.theName
  def type(self): return self.theType
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def environmentProperties(self): return self.theEnvironmentProperties
