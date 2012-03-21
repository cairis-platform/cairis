#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetEnvironmentProperties.py $ $Id: AssetEnvironmentProperties.py 424 2011-02-25 21:29:47Z shaf $
from EnvironmentProperties import EnvironmentProperties

class AssetEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,syProperties,pRationale,associations=[]):
    EnvironmentProperties.__init__(self,environmentName)
    self.theProperties = syProperties
    self.theRationale = pRationale
    self.theAssociations = associations

  def properties(self): return self.theProperties
  def rationale(self): return self.theRationale
  def associations(self): return self.theAssociations
