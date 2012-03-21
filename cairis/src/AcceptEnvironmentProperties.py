#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AcceptEnvironmentProperties.py $ $Id: AcceptEnvironmentProperties.py 330 2010-10-31 15:01:28Z shaf $
from EnvironmentProperties import EnvironmentProperties

class AcceptEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,cost = '',rationale = ''):
    EnvironmentProperties.__init__(self,environmentName)
    self.theCost = cost
    self.theRationale = rationale

  def cost(self): return self.theCost
  def description(self): return self.theRationale
