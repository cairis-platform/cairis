#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Risk.py $ $Id: Risk.py 249 2010-05-30 17:07:31Z shaf $
class Risk:
  def __init__(self,riskId,riskName,threatName,vulName,mc=None):
    self.theId = riskId
    self.theName = riskName
    self.theThreatName = threatName
    self.theVulnerabilityName = vulName
    self.theMisuseCase = mc

  def id(self): return self.theId
  def name(self): return self.theName
  def threat(self): return self.theThreatName
  def vulnerability(self): return self.theVulnerabilityName
  def misuseCase(self): return self.theMisuseCase
