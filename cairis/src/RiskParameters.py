#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RiskParameters.py $ $Id: RiskParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class RiskParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,riskName,threatName,vulName,mc):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theRiskName = riskName
    self.theThreatName = threatName
    self.theVulnerabilityName = vulName
    self.theMisuseCase = mc

  def name(self): return self.theRiskName
  def threat(self): return self.theThreatName
  def vulnerability(self): return self.theVulnerabilityName
  def misuseCase(self): return self.theMisuseCase
