#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AttackerEnvironmentProperties.py $ $Id: AttackerEnvironmentProperties.py 330 2010-10-31 15:01:28Z shaf $
from EnvironmentProperties import EnvironmentProperties

class AttackerEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,roles,motives,capabilities):
    EnvironmentProperties.__init__(self,environmentName)
    self.theRoles = roles
    self.theMotives = motives
    self.theCapabilities = capabilities 

  def roles(self): return self.theRoles
  def motives(self): return self.theMotives
  def capabilities(self): return self.theCapabilities
