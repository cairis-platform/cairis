#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MisuseCase.py $ $Id: MisuseCase.py 249 2010-05-30 17:07:31Z shaf $
class MisuseCase:
  def __init__(self,mcId,mcName,cProps,riskName):
    self.theId = mcId
    self.theName = mcName
    self.theEnvironmentProperties = cProps
    self.theRiskName = riskName
    self.theThreatName = ''
    self.theVulnerabilityName = ''
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p

  def environmentProperties(self): return self.theEnvironmentProperties

  def id(self): return self.theId
  def name(self): return self.theName
  def risk(self): return self.theRiskName
  def threat(self): return self.theThreatName
  def vulnerability(self): return self.theVulnerabilityName

  def narrative(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).narrative()
    else:
      workingNarrative = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingNarrative += p.narrative()
        if (noOfEnvironments > 1):
          workingNarrative += ' [' + environmentName + '].  '
      return workingNarrative
