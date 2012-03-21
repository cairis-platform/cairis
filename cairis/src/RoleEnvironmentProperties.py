#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RoleEnvironmentProperties.py $ $Id: RoleEnvironmentProperties.py 249 2010-05-30 17:07:31Z shaf $
from EnvironmentProperties import EnvironmentProperties

class RoleEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,responses,countermeasures):
    EnvironmentProperties.__init__(self,environmentName)
    self.theResponses = responses
    self.theCountermeasures = countermeasures

  def responses(self): return self.theResponses
  def countermeasures(self): return self.theCountermeasures
