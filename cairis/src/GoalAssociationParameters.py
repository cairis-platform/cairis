#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalAssociationParameters.py $ $Id: GoalAssociationParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class GoalAssociationParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,envName,goalName,goalDimName,aType,subGoalName='',subGoalDimName='',alternativeId=0,rationale=''):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theEnvironmentName = envName
    self.theGoal = goalName
    self.theGoalDimension = goalDimName
    self.theAssociationType = aType
    self.theSubGoal = subGoalName
    self.theSubGoalDimension = subGoalDimName
    self.theAlternativeId = alternativeId
    self.theRationale = rationale

  def environment(self): return self.theEnvironmentName
  def goal(self): return self.theGoal
  def goalDimension(self): return self.theGoalDimension
  def type(self): return self.theAssociationType
  def subGoal(self): return self.theSubGoal
  def subGoalDimension(self): return self.theSubGoalDimension
  def alternative(self): return self.theAlternativeId
  def rationale(self): return self.theRationale
