#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalEnvironmentProperties.py $ $Id: GoalEnvironmentProperties.py 509 2011-10-30 14:27:19Z shaf $
from EnvironmentProperties import EnvironmentProperties

class GoalEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,lbl='',definition='',category='',priority='',fitCriterion='',issue='',goalRefinements=[],subGoalRefinements=[],concs=[],cas=[]):
    EnvironmentProperties.__init__(self,environmentName)
    self.theLabel = lbl
    self.theDefinition = definition
    self.theCategory = category
    self.thePriority = priority
    self.theFitCriterion = fitCriterion
    self.theIssue = issue
    self.theGoalRefinements = goalRefinements
    self.theSubGoalRefinements = subGoalRefinements
    self.theConcerns = concs
    self.theConcernAssociations = cas

  def label(self): return self.theLabel
  def definition(self): return self.theDefinition
  def category(self): return self.theCategory
  def priority(self): return self.thePriority
  def fitCriterion(self): return self.theFitCriterion
  def issue(self): return self.theIssue
  def goalRefinements(self): return self.theGoalRefinements
  def subGoalRefinements(self): return self.theSubGoalRefinements
  def concerns(self): return self.theConcerns
  def concernAssociations(self): return self.theConcernAssociations

  def setDefinition(self,v): self.theDefinition = v
  def setCategory(self,v): self.theCategory = v
  def setPriority(self,v): self.thePriority = v
  def setFitCriterion(self,v): self.theFitCriterion = v
  def setIssue(self,v): self.theIssue = v
