#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaParameters.py $ $Id: PersonaParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class PersonaParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,name,activities,attitudes,aptitudes,motivations,skills,image,isAssumption,pType,properties):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = name
    self.theActivities = activities
    self.theAttitudes = attitudes
    self.theAptitudes = aptitudes
    self.theMotivations = motivations
    self.theSkills = skills
    self.theImage = image
    self.isAssumption = isAssumption
    self.thePersonaType = pType
    self.theEnvironmentProperties = properties

  def name(self): return self.theName
  def attitudes(self): return self.theAttitudes
  def activities(self): return self.theActivities
  def aptitudes(self): return self.theAptitudes
  def motivations(self): return self.theMotivations
  def skills(self): return self.theSkills
  def image(self): return self.theImage
  def assumption(self): return self.isAssumption
  def type(self): return self.thePersonaType
  def environmentProperties(self): return self.theEnvironmentProperties
