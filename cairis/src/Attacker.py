#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Attacker.py $ $Id: Attacker.py 330 2010-10-31 15:01:28Z shaf $
from AttackerEnvironmentProperties import AttackerEnvironmentProperties

class Attacker:
  def __init__(self,attackerId,attackerName,attackerDescription,attackerImage,environmentProperties):
    self.theId = attackerId
    self.theName = attackerName
    self.theDescription = attackerDescription
    self.theImage = attackerImage
    self.theEnvironmentProperties = environmentProperties
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p

  def id(self): return self.theId
  def name(self): return self.theName
  def description(self): return self.theDescription 
  def image(self): return self.theImage
  def environmentProperties(self): return self.theEnvironmentProperties

  def roles(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).roles()
    else:
      mergedRoles = []
      for p in self.theEnvironmentProperties:
        mergedRoles += p.roles()
      return set(mergedRoles)

  def motives(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).motives()
    else:
      mergedMotives = []
      for p in self.theEnvironmentProperties:
        mergedMotives += p.motives()
      return set(mergedMotives)

  def capability(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).capabilities()
    else:
      mergedCapability = []
      for p in self.theEnvironmentProperties:
        mergedCapability += p.capabilities()
      return set(mergedCapability)
