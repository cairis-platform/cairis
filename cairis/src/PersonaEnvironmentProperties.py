#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaEnvironmentProperties.py $ $Id: PersonaEnvironmentProperties.py 249 2010-05-30 17:07:31Z shaf $
from EnvironmentProperties import EnvironmentProperties

class PersonaEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,direct=False,description='',roles=[]):
    EnvironmentProperties.__init__(self,environmentName)
    self.theDirectFlag = direct 
    self.theNarrative = description
    self.theRoles = roles

  def directFlag(self): return self.theDirectFlag
  def narrative(self): return self.theNarrative
  def roles(self): return self.theRoles
