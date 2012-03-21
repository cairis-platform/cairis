#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CountermeasureParameters.py $ $Id: CountermeasureParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class CountermeasureParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,cmName,cmDesc,cmType,cProps):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = cmName
    self.theDescription = cmDesc
    self.theType = cmType
    self.theEnvironmentProperties = cProps

  def name(self): return self.theName
  def type(self): return self.theType
  def description(self): return self.theDescription
  def environmentProperties(self): return self.theEnvironmentProperties
