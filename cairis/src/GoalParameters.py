#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalParameters.py $ $Id: GoalParameters.py 406 2011-01-13 00:25:07Z shaf $
import ObjectCreationParameters

class GoalParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,goalName,goalOrig,properties):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = goalName
    self.theOriginator = goalOrig
    self.theEnvironmentProperties = properties

  def name(self): return self.theName
  def originator(self): return self.theOriginator
  def environmentProperties(self): return self.theEnvironmentProperties
