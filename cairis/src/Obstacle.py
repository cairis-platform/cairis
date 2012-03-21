#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Obstacle.py $ $Id: Obstacle.py 509 2011-10-30 14:27:19Z shaf $
from ObstacleEnvironmentProperties import ObstacleEnvironmentProperties

class Obstacle:
  def __init__(self,obsId,obsName,obsOrig,environmentProperties):
    self.theId = obsId
    self.theName = obsName
    self.theOriginator = obsOrig
    self.theEnvironmentProperties = environmentProperties
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p

  def id(self): return self.theId
  def setId(self,v): self.theId = v
  def name(self): return self.theName
  def originator(self): return self.theOriginator
  def environmentProperties(self): return self.theEnvironmentProperties
  def environmentProperty(self,envName): return self.theEnvironmentDictionary[envName]

  def label(self,environmentName):
    return (self.theEnvironmentDictionary[environmentName]).label()

  def definition(self,environmentName,dupProperty=''):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).definition()
    else:
      workingAttr = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingAttr += p.definition()
        if (noOfEnvironments > 1):
          workingAttr += ' [' + environmentName + '].  '
      return workingAttr

  def category(self,environmentName,dupProperty=''):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).category()
    else:
      workingAttr = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingAttr += p.category()
        if (noOfEnvironments > 1):
          workingAttr += ' [' + environmentName + '].  '
      return workingAttr

  def setName(self, v):
    self.theName = v

  def setOriginator(self, v):
    self.theOriginator = v

  def setDefinition(self,environmentName,v):
    (self.theEnvironmentDictionary[environmentName]).setDefinition(v)

  def setCategory(self,environmentName,v):
    (self.theEnvironmentDictionary[environmentName]).setCategory(v)

  def refinements(self,environmentName):
    for assoc in ((self.theEnvironmentDictionary[environmentName]).subGoalRefinements()):
      if assoc[1] == 'obstacle':
        return True
    return False

