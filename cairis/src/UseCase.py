#$URL$ $Id: UseCase.py 530 2011-11-16 19:29:16Z shaf $

class UseCase:
  def __init__(self,ucId,ucName,ucAuth,ucCode,ucActors,ucDesc,cProps):
    self.theId = ucId
    self.theName = ucName
    self.theAuthor = ucAuth
    self.theCode = ucCode
    self.theActors = ucActors
    self.theDescription = ucDesc
    self.theEnvironmentProperties = cProps
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p

  def environmentProperties(self): return self.theEnvironmentProperties

  def id(self): return self.theId
  def name(self): return self.theName
  def author(self): return self.theAuthor
  def code(self): return self.theCode
  def actors(self): return self.theActors
  def description(self): return self.theDescription

  def steps(self,environmentName,dupProperty = ''):
    return (self.theEnvironmentDictionary[environmentName]).steps()

  def preconditions(self,environmentName,dupProperty = ''):
    return (self.theEnvironmentDictionary[environmentName]).preconditions()

  def postconditions(self,environmentName,dupProperty = ''):
    return (self.theEnvironmentDictionary[environmentName]).postconditions()
