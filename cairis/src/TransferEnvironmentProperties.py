#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TransferEnvironmentProperties.py $ $Id: TransferEnvironmentProperties.py 249 2010-05-30 17:07:31Z shaf $
from EnvironmentProperties import EnvironmentProperties

class TransferEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,rationale = '',roles = []):
    EnvironmentProperties.__init__(self,environmentName)
    self.theRationale = rationale
    self.theRoles = roles

  def description(self): return self.theRationale
  def roles(self): return self.theRoles
