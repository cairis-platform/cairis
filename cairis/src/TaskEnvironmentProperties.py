#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskEnvironmentProperties.py $ $Id: TaskEnvironmentProperties.py 532 2011-11-17 15:47:35Z shaf $
from EnvironmentProperties import EnvironmentProperties

class TaskEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,deps = '',personas = [],assets = [],concs=[],narrative = '',consequences = '', benefits = ''):
    EnvironmentProperties.__init__(self,environmentName)
    self.thePersonas = personas
    self.theAssets = assets
    self.theDependencies = deps
    self.theNarrative = narrative
    self.theConsequences = consequences
    self.theBenefits = benefits
    self.theConcernAssociations = concs

  def personas(self): return self.thePersonas
  def assets(self): return self.theAssets
  def narrative(self): return self.theNarrative
  def consequences(self): return self.theConsequences
  def benefits(self): return self.theBenefits
  def dependencies(self): return self.theDependencies
  def concernAssociations(self): return self.theConcernAssociations
