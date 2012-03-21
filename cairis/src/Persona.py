#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Persona.py $ $Id: Persona.py 249 2010-05-30 17:07:31Z shaf $
class Persona:
  def __init__(self,personaId,personaName,pActivities,pAttitudes,pAptitudes,pMotivations,pSkills,image,isAssumption,pType,environmentProperties):
    self.theId = personaId
    self.theName = personaName
    self.theActivities = pActivities
    self.theAttitudes = pAttitudes
    self.theAptitudes = pAptitudes
    self.theMotivations = pMotivations
    self.theSkills = pSkills
    self.theImage = image
    self.isAssumption = isAssumption
    self.thePersonaType = pType
    self.theEnvironmentProperties = environmentProperties
    self.theEnvironmentDictionary = {}
    for p in self.theEnvironmentProperties:
      environmentName = p.name()
      self.theEnvironmentDictionary[environmentName] = p

  def id(self): return self.theId
  def name(self): return self.theName
  def activities(self): return self.theActivities
  def attitudes(self): return self.theAttitudes
  def aptitudes(self): return self.theAptitudes
  def motivations(self): return self.theMotivations
  def skills(self): return self.theSkills
  def image(self): return self.theImage
  def assumption(self): return self.isAssumption
  def type(self): return self.thePersonaType
  def environmentProperties(self): return self.theEnvironmentProperties

  def narrative(self,environmentName,dupProperty):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).narrative()
    else:
      workingDescription = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingDescription += p.narrative()
        if (noOfEnvironments > 1):
          workingDescription += ' [' + environmentName + '].  '
      return workingDescription

  def directFlag(self,environmentName,dupProperty): 
    if (dupProperty == ''):
      return str((self.theEnvironmentDictionary[environmentName]).directFlag())
    else:
      workingDirect = ''
      noOfEnvironments = len(self.theEnvironmentProperties)
      for p in self.theEnvironmentProperties:
        environmentName = p.name()
        workingDirect += p.directFlag()
        if (noOfEnvironments > 1):
          workingDirect += ' [' + environmentName + '].  '
      return workingDirect


  def roles(self,environmentName,dupProperty):
    if (dupProperty == ''):
      return (self.theEnvironmentDictionary[environmentName]).roles()
    else:
      mergedRoles = []
      for p in self.theEnvironmentProperties:
        mergedRoles += p.roles()
      return set(mergedRoles)
