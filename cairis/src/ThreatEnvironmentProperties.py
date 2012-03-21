#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ThreatEnvironmentProperties.py $ $Id: ThreatEnvironmentProperties.py 425 2011-02-26 12:38:39Z shaf $
from EnvironmentProperties import EnvironmentProperties

class ThreatEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,lhood,assets,attackers,syProperties,pRationale):
    EnvironmentProperties.__init__(self,environmentName)
    self.theLikelihood = lhood
    self.theAssets = assets
    self.theAttackers = attackers
    self.theProperties = syProperties
    self.theRationale = pRationale

  def likelihood(self): return self.theLikelihood
  def assets(self): return self.theAssets
  def attackers(self): return self.theAttackers
  def properties(self): return self.theProperties
  def rationale(self): return self.theRationale
