#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalAssociation.py $ $Id: GoalAssociation.py 249 2010-05-30 17:07:31Z shaf $
class GoalAssociation:
  def __init__(self,associationId,envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale):
    self.theId = associationId
    self.theEnvironmentName = envName
    self.theGoal = goalName
    self.theGoalDimension = goalDimName
    self.theAssociationType = aType
    self.theSubGoal = subGoalName
    self.theSubGoalDimension = subGoalDimName
    self.theAlternativeId = alternativeId
    self.theRationale = rationale

  def id(self): return self.theId
  def environment(self): return self.theEnvironmentName
  def goal(self): return self.theGoal
  def goalDimension(self): return self.theGoalDimension
  def type(self): return self.theAssociationType
  def subGoal(self): return self.theSubGoal
  def subGoalDimension(self): return self.theSubGoalDimension
  def alternative(self): return self.theAlternativeId
  def rationale(self): return self.theRationale

  def __str__(self): return self.theEnvironmentName + ' / ' + self.theGoal + ' / '  + self.theGoalDimension + ' / ' + self.theAssociationType + ' / ' + self.theSubGoal + ' / ' + self.theSubGoalDimension + ' / ' + str(self.theAlternativeId)
