#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskParameters.py $ $Id: TaskParameters.py 572 2012-03-16 21:37:33Z shaf $
import ObjectCreationParameters

class TaskParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,tName,tSName,tObjt,isAssumption,tAuth,cProps):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = tName
    self.theShortCode = tSName
    self.theObjective = tObjt
    self.isAssumption = isAssumption
    self.theAuthor = tAuth
    self.theEnvironmentProperties = cProps

  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def objective(self): return self.theObjective
  def assumption(self): return self.isAssumption
  def author(self): return self.theAuthor
  def environmentProperties(self): return self.theEnvironmentProperties
