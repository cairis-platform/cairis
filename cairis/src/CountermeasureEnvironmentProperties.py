#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CountermeasureEnvironmentProperties.py $ $Id: CountermeasureEnvironmentProperties.py 425 2011-02-26 12:38:39Z shaf $
from EnvironmentProperties import EnvironmentProperties
from numpy import *

class CountermeasureEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,requirements = [],targets = [],properties = array((0,0,0,0,0,0,0,0)),rationale = ['None','None','None','None','None','None','None','None'],cost = '', roles = [], personas = {}):
    EnvironmentProperties.__init__(self,environmentName)
    self.theRequirements = requirements
    self.theTargets = targets
    self.theProperties = properties
    self.theRationale = rationale
    self.theCost = cost
    self.theRoles = roles
    self.thePersonas = personas

  def requirements(self): return self.theRequirements
  def targets(self): return self.theTargets
  def properties(self): return self.theProperties
  def rationale(self): return self.theRationale
  def cost(self): return self.theCost
  def roles(self): return self.theRoles
  def personas(self): return self.thePersonas
