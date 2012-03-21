#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MisuseCaseEnvironmentProperties.py $ $Id: MisuseCaseEnvironmentProperties.py 249 2010-05-30 17:07:31Z shaf $
from EnvironmentProperties import EnvironmentProperties

class MisuseCaseEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,narrative = ''):
    EnvironmentProperties.__init__(self,environmentName)
    self.theDescription = narrative

  def narrative(self): return self.theDescription
