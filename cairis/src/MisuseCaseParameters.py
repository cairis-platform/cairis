#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MisuseCaseParameters.py $ $Id: MisuseCaseParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class MisuseCaseParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,scName,cProps,risk):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = scName
    self.theRisk = risk
    self.theEnvironmentProperties = cProps

  def name(self): return self.theName
  def risk(self): return self.theRisk
  def environmentProperties(self): return self.theEnvironmentProperties
