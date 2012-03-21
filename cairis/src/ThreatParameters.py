#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ThreatParameters.py $ $Id: ThreatParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class ThreatParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,threatName,thrType,thrMethod,cProperties):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = threatName
    self.theType = thrType
    self.theMethod = thrMethod
    self.theEnvironmentProperties = cProperties

  def name(self): return self.theName
  def type(self): return self.theType
  def method(self): return self.theMethod
  def environmentProperties(self): return self.theEnvironmentProperties
