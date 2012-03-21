#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ResponseParameters.py $ $Id: ResponseParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class ResponseParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,respName,respRisk,cProps,rType):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = respName
    self.theRisk = respRisk
    self.theEnvironmentProperties = cProps
    self.theResponseType = rType

  def name(self): return self.theName
  def risk(self): return self.theRisk
  def environmentProperties(self): return self.theEnvironmentProperties
  def responseType(self): return self.theResponseType
