#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ObstacleEnvironmentProperties.py $ $Id: ObstacleEnvironmentProperties.py 509 2011-10-30 14:27:19Z shaf $
from EnvironmentProperties import EnvironmentProperties

class ObstacleEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,lbl='',definition='',category='',gRefs=[], sgRefs=[], concs=[]):
    EnvironmentProperties.__init__(self,environmentName)
    self.theLabel = lbl
    self.theDefinition = definition
    self.theCategory = category
    self.theGoalRefinements = gRefs
    self.theSubGoalRefinements = sgRefs
    self.theConcerns = concs

  def label(self): return self.theLabel
  def definition(self): return self.theDefinition
  def category(self): return self.theCategory
  def goalRefinements(self): return self.theGoalRefinements
  def subGoalRefinements(self): return self.theSubGoalRefinements
  def concerns(self): return self.theConcerns

  def setDefinition(self,v): self.theDefinition = v
  def setCategory(self,v): self.theCategory = v
